from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "monitoring.db")
SCRIPT_PATH = os.path.join(BASE_DIR, "run_tests.py"

@app.get("/")
def consignes():
     return render_template('consignes.html')

if __name__ == "__main__":
    # utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True)

# ... garde tes imports actuels ...
@app.route('/test')
def test_dashboard():
    history = []
    history_reversed = []
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # On récupère les 30 derniers tests
        history = conn.execute("SELECT * FROM runs ORDER BY timestamp DESC LIMIT 30").fetchall()
        conn.close()
        history_reversed = list(reversed(history))
    except Exception as e:
        print(f"Erreur de lecture DB : {e}")

    return render_template("index.html", runs=history, chart_data=history_reversed)

@app.route('/run-manual-test')
def run_manual_test():
    try:
        # On force l'exécution du script python
        subprocess.run(["python3", SCRIPT_PATH], check=True)
    except Exception as e:
        print(f"Erreur lors de l'exécution du test : {e}")
    
    return redirect(url_for('test_dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
