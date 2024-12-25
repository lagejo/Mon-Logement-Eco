import sqlite3
from datetime import datetime
import logging
import requests

def save_capteur_data(temperature: float, humidity: float):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    date_today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c.execute("INSERT INTO Mesure (valeur, date_insert, id_capteur) VALUES (?, ?, ?)", (temperature, date_today, 1))
        c.execute("INSERT INTO Mesure (valeur, date_insert, id_capteur) VALUES (?, ?, ?)", (humidity, date_today, 2))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_factures(logement_id=None):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    
    if logement_id:
        c.execute("SELECT type_facture, montant FROM Facture WHERE id_loge = ?", (logement_id,))
    else:
        c.execute("SELECT type_facture, montant FROM Facture")
        
    rows = c.fetchall()
    conn.close()
    
    return [{"type_facture": row[0], "montant": row[1]} for row in rows]

def get_capteur_data(id_capteur: int):
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT valeur, date_insert FROM Mesure WHERE id_capteur = ? ORDER BY date_insert DESC LIMIT 5", (id_capteur,))
    data = c.fetchall()
    conn.close()
    return data

def get_capteurs():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT Capteur.*, Piece.nom AS piece_nom, Logement.adresse AS logement_adresse
        FROM Capteur
        JOIN Piece ON Capteur.id_piece = Piece.id_piece
        JOIN Logement ON Piece.id_loge = Logement.id_loge
    """)
    capteurs = c.fetchall()
    conn.close()
    return capteurs

def get_pieces_with_logement():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT Piece.id_piece, Piece.nom, Piece.x, Piece.y, Piece.z, Logement.adresse AS logement_adresse
        FROM Piece
        JOIN Logement ON Piece.id_loge = Logement.id_loge
    """)
    pieces = c.fetchall()
    conn.close()
    return pieces

def get_pieces():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM Piece")
    pieces = c.fetchall()
    conn.close()
    return pieces

def get_logements():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM Logement")
    logements = c.fetchall()
    conn.close()
    return logements

#Question 2.3 des TP
def get_meteo():
    api_key = "53eb9e8ea37324aaf87898c6bea832ab"  # Ma clé de l'API (openweathermap)
    lat = 48.8566  # Latitude Paris
    lon = 2.3522   # Longitude Paris
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Données météo OK")
        return response.json()
    else:
        logging.error(f"Failed : {response.status_code}")
        return None