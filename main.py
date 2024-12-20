from fastapi import FastAPI, Request, HTTPException, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import logging
import requests


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class SensorData(BaseModel):
    temperature: float
    humidity: float

def save_sensor_data(temperature: float, humidity: float):
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

@app.post("/sensor")
async def receive_sensor_data(data: SensorData):
    try:
        save_sensor_data(data.temperature, data.humidity)
        return {"message": "Sensor data received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_factures():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT type_facture, montant FROM Facture")
    factures = c.fetchall()
    conn.close()
    return factures

def get_sensor_data(id_capteur: int):
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

@app.post("/add_capteur")
async def add_capteur(ref_commerciale: str = Form(...), port_communication: str = Form(...), type_capteur: int = Form(...), piece: int = Form(...)):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    date_insert = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c.execute("INSERT INTO Capteur (ref_commerciale, port_communication, date_insert, id_type, id_piece) VALUES (?, ?, ?, ?, ?)",
                  (ref_commerciale, port_communication, date_insert, type_capteur, piece))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

@app.get("/etatcapteur", response_class=HTMLResponse)
async def read_etat_capteur(request: Request):
    temperature_data = get_sensor_data(1)
    humidity_data = get_sensor_data(2)
    return templates.TemplateResponse("etat_capteur.html", {
        "request": request,
        "temperature_data": temperature_data,
        "humidity_data": humidity_data
    })

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    weather_forecast = get_weather_forecast()
    return templates.TemplateResponse("index.html", {"request": request, "weather_forecast": weather_forecast})

@app.get("/economie", response_class=HTMLResponse)
async def read_consommation(request: Request):
    logements = get_logements()
    return templates.TemplateResponse("eco.html", {"request": request, "logements": logements})

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


@app.get("/config", response_class=HTMLResponse)
async def read_config(request: Request):
    capteurs = get_capteurs()
    logements = get_logements()
    pieces = get_pieces_with_logement()
    return templates.TemplateResponse("config.html", {"request": request, "capteurs": capteurs, "logements": logements, "pieces": pieces})

@app.get("/consommation", response_class=HTMLResponse)
async def afficher_economie(request: Request):
    factures = get_factures()
    labels = [facture['type_facture'] for facture in factures]
    data = [facture['montant'] for facture in factures]

    return templates.TemplateResponse("conso.html", {
        "request": request,
        "labels": labels,
        "data": data,
        "zip": zip  # Passer la fonction zip au contexte
    })

def get_logements():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM Logement")
    logements = c.fetchall()
    conn.close()
    return logements

@app.get("/get_pieces")
async def get_pieces(logement_id: int = Query(...)):
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id_piece, nom FROM Piece WHERE id_loge = ?", (logement_id,))
    pieces = c.fetchall()
    conn.close()
    return JSONResponse(content={"pieces": [dict(piece) for piece in pieces]})

@app.post("/ajouter_piece")
async def ajouter_piece(nom_piece: str = Form(...), x: float = Form(...), y: float = Form(...), z: float = Form(...), logement: int = Form(...)):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        query = '''INSERT INTO Piece (nom, x, y, z, id_loge)
                   VALUES (?, ?, ?, ?, ?)'''
        c.execute(query, (nom_piece, x, y, z, logement))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

@app.post("/ajouter_logement")
async def ajouter_piece(adresse: str = Form(...), numero_tel: str = Form(...), IP: str = Form(...), date_insert: str = Form(...)):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        query = '''INSERT INTO Logement (adresse, numero_tel, IP, date_insert)
                   VALUES (?, ?, ?, ?)'''
        c.execute(query, (adresse, numero_tel, IP, date_insert))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

#ajouter une facture, page économie
@app.post("/ajouter_facture")
async def ajouter_facture(type_facture: str = Form(...), montant: float = Form(...), valeur_conso: float = Form(...), date_fact: str = Form(...), id_loge: int = Form(...)):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        query = '''INSERT INTO Facture (type_facture, montant, valeur_conso, date_fact, id_loge)
                   VALUES (?, ?, ?, ?, ?)'''
        c.execute(query, (type_facture, montant, valeur_conso, date_fact, id_loge))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    return RedirectResponse(url="/economie", status_code=303)

@app.post("/supprimer_logement")
async def supprimer_logement(logement: int = Form(...)):
    print(f"Suppression du logement avec id: {logement}")
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM Logement WHERE id_loge = ?", (logement,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

@app.post("/supprimer_piece")
async def supprimer_piece(piece: str = Form(...)):
    print(f"Suppression de la pièce avec id: {piece}")
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM Piece WHERE id_piece = ?", (piece,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

@app.post("/supprimer_capteur")
async def supprimer_capteur(capteur: int = Form(...)):
    print(f"Suppression du capteur avec id: {capteur}")
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM Capteur WHERE id_capteur = ?", (capteur,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

logging.basicConfig(level=logging.INFO)

def get_weather_forecast():
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

    #bash : uvicorn serveur_remplissage:app --reload --host 0.0.0.0 --port 8000