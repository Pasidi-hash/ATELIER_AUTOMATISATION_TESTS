from flask import Flask, render_template, redirect, url_for
import sqlite3
import os
import subprocess

app = Flask(__name__)

# CONFIGURATION DES CHEMINS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "monitoring.db")
# Correction ici : ajout de la parenthèse fermante manquante )
SCRIPT_PATH = os.path.join(BASE_DIR, "run_tests.py")

@app.route("/")
def consignes():
    return render_template('consignes.html')

@app.route('/test')
def test_dashboard():
    history = []
    history_reversed = []
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # Récupère les 30 derniers tests
        history = conn.execute("SELECT * FROM runs ORDER BY timestamp DESC LIMIT 30").fetchall()
        conn.close()
        history_reversed = list(reversed(history))
    except Exception as e:
        print(f"Erreur de lecture DB : {e}")

    # On envoie bien history ET history_reversed (chart_data)
    return render_template("index.html", runs=history, chart_data=history_reversed)

@app.route('/run-manual-test')
def run_manual_test():
    try:
        # On utilise python3 pour s'assurer de l'exécution sur PythonAnywhere
        subprocess.run(["python3", SCRIPT_PATH], check=True)
    except Exception as e:
        print(f"Erreur lors de l'exécution du test : {e}")
    
    return redirect(url_for('test_dashboard'))

# IMPORTANT : Ce bloc doit TOUJOURS être à la toute fin du fichier
if __name__ == "__main__":
    app.run(debug=True)
