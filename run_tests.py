import requests
import time
import sqlite3
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- CONFIGURATION ---
# On utilise l'API Frankfurter (Taux de change)
API_URL = "https://api.frankfurter.app/latest"
# Le fichier SQLite sera créé au même endroit que le script
DB_PATH = os.path.join(os.path.dirname(__file__), "monitoring.db")

def init_db():
    """Initialise la base de données SQLite (Point 6)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            api_name TEXT,
            status TEXT,
            latency FLOAT
        )
    ''')
    conn.commit()
    conn.close()

def run_monitoring():
    """Exécute le test, mesure la QoS et gère la robustesse (Points 2, 3, 4)"""
    # 1. Configuration de la robustesse (Point 3 : Retry & Timeout)
    session = requests.Session()
    retry_strategy = Retry(
        total=3, # 3 tentatives max
        backoff_factor=1, # Attend 1s, 2s, 4s entre les essais
        status_forcelist=[429, 500, 502, 503, 504] # Erreurs qui déclenchent un retry
    )
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    start_time = time.time()
    status = "UNKNOWN"
    
    try:
        # Exécution de la requête avec un timeout de 5 secondes (Point 4 : QoS)
        response = session.get(API_URL, timeout=5)
        latency = round(time.time() - start_time, 3)
        
        # 2. Vérification du contrat (Point 2 : Assertions)
        if response.status_code == 200:
            data = response.json()
            # On vérifie que les champs attendus sont là
            if "rates" in data and "base" in data:
                status = "SUCCESS"
            else:
                status = "FAILED (Missing Fields)"
        else:
            status = f"FAILED (HTTP {response.status_code})"

    except requests.exceptions.Timeout:
        status = "ERROR (Timeout)"
        latency = 5.0
    except Exception as e:
        status = f"ERROR ({type(e).__name__})"
        latency = round(time.time() - start_time, 3)

    # 3. Sauvegarde en base de données (Point 6)
    save_to_db(status, latency)
    print(f"Test terminé : {status} | Latence : {latency}s")

def save_to_db(status, latency):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO runs (api_name, status, latency) VALUES (?, ?, ?)",
        ("Frankfurter", status, latency)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    run_monitoring()
