from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)

@app.get("/")
def consignes():
     return render_template('consignes.html')

if __name__ == "__main__":
    # utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True)

# ... garde tes imports actuels ...

# Définition du chemin vers la base (à mettre en haut du fichier)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "monitoring.db")

# --- TA NOUVELLE PAGE TEST ---
@app.route('/test')
def test_dashboard():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        # On récupère les résultats des tests pour le dashboard
        history = conn.execute("SELECT * FROM runs ORDER BY timestamp DESC LIMIT 20").fetchall()
    except sqlite3.OperationalError:
        history = []
    conn.close()
    
    # On utilise le template index.html que tu as déjà créé
    return render_template("index.html", runs=history)

# ... garde ton app.run() ...
