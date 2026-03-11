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

@app.route('/test')
def test_dashboard():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        # On récupère les 30 derniers runs pour avoir assez de points sur le graphique
        history = conn.execute("SELECT * FROM runs ORDER BY timestamp DESC LIMIT 30").fetchall()
    except sqlite3.OperationalError:
        history = []
    conn.close()
    
    # On inverse l'ordre pour le graphique (chronologique de gauche à droite)
    history_reversed = list(reversed(history))
    
    return render_template("index.html", runs=history, chart_data=history_reversed)
