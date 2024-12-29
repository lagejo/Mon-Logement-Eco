from fastapi import FastAPI, Request, HTTPException, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
from collections import defaultdict
from typing import Optional
from utils import *
from datetime import datetime


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Data_capteur(BaseModel):
    temperature: float
    humidity: float

@app.post("/capteur")
async def receive_capteur(data: Data_capteur):
    try:
        save_capteur_data(data.temperature, data.humidity)
        return {"message": "Données du capteur bien reçues"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

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

@app.post("/add_actionneur")
async def add_capteur(ref_commerciale: str = Form(...), port_communication: str = Form(...), id_type: int = Form(...), piece: int = Form(...)):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    date_insert = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        c.execute("INSERT INTO Actionneur (ref_commerciale, port_communication, date_insert, id_type, id_piece) VALUES (?, ?, ?, ?, ?)",
                  (ref_commerciale, port_communication, date_insert, id_type, piece))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

@app.post("/ajouter_type_capteur")
async def ajouter_type_capteur(unite_mesure: str = Form(...)):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        query = '''INSERT INTO Type_capteur (unite_mesure)
                   VALUES (?)'''
        c.execute(query, (unite_mesure,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

@app.get("/etatcapteur", response_class=HTMLResponse)
async def read_etat_capteur(request: Request):
    #les deux capteurs que j'ai configurés et testés, il s'agit du dht11 branché sur un esp8266
    #il est décomposé en deux capteurs, un pour la température et un pour l'humidité
    # temperature_data = get_capteur_data(2)
    # humidity_data = get_capteur_data(1)
    capteurs = get_capteurs()
    logements = get_logements()
    pieces = get_pieces_with_logement()
    types_capteurs = get_types_capteurs()
    active_capteurs = get_active_capteurs() 
    inactive_capteurs = get_inactive_capteurs() 
    actionneurs = get_actionneurs()
    return templates.TemplateResponse("etat_capteur.html", {
        "request": request,
        "capteurs": capteurs,
        "logements": logements,
        "pieces": pieces,
        "types_capteurs": types_capteurs,
        "active_capteurs": active_capteurs,
        "inactive_capteurs": inactive_capteurs,
        "actionneurs": actionneurs
    })

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    weather_forecast = get_meteo()
    return templates.TemplateResponse("accueil.html", {"request": request, "weather_forecast": weather_forecast})

@app.get("/economie", response_class=HTMLResponse)
async def read_consommation(request: Request):
    logements = get_logements()
    return templates.TemplateResponse("eco.html", {"request": request, "logements": logements})

@app.get("/get_facture_types")
async def get_facture_types(logement_id: int):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    
    c.execute("""
        SELECT DISTINCT type_facture 
        FROM Facture 
        WHERE id_loge = ?
    """, (logement_id,))
    
    types = [row[0] for row in c.fetchall()]
    conn.close()
    
    return {"types": types}

@app.get("/get_facturesjson")
async def get_facturesjson(facture_type_id: str, logement_id: str):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    c.execute("""
        SELECT montant, date_fact
        FROM Facture
        WHERE type_facture = ?
        AND id_loge = ?
        ORDER BY date_fact DESC LIMIT 5
    """, (facture_type_id,logement_id))
    rows = c.fetchall()
    conn.close()
    
    return {
        "montants": [r[0] for r in rows],
        "dates": [r[1] for r in rows]
    }

@app.get("/config", response_class=HTMLResponse)
async def read_config(request: Request):
    capteurs = get_capteurs()
    logements = get_logements()
    pieces = get_pieces_with_logement()
    types_capteurs = get_types_capteurs()  
    actionneurs = get_actionneurs()
    return templates.TemplateResponse("config.html", {"request": request, "capteurs": capteurs, "logements": logements, "pieces": pieces, "types_capteurs": types_capteurs, "actionneurs": actionneurs})


@app.get("/consommation")
async def afficher_economie(
    request: Request,
    logement_id: Optional[str] = None
):
    logements = get_logements()
    factures = []
    total_factures = 0
    
    try:
        selected_id = int(logement_id) if logement_id else None
    except ValueError:
        selected_id = None
    
    if selected_id:
        factures = get_factures(selected_id)
    
    # Données pour le graphique camembert
    facture_dict = defaultdict(float)
    # Données pour le graphique d'évolution
    types_facture = set()
    dates_uniques = set()
    valeurs_par_date_type = {}
    
    if factures:
        for facture in factures:
            # Pour le camembert
            facture_dict[facture['type_facture']] += facture['montant']
            
            # Pour le graphique d'évolution
            types_facture.add(facture['type_facture'])
            
            # Handle date
            date_facture = facture.get('date_facture')
            if date_facture:
                date_str = date_facture  # Assuming date_facture is already in 'YYYY-MM-DD' format
                dates_uniques.add(date_str)
                
                if date_str not in valeurs_par_date_type:
                    valeurs_par_date_type[date_str] = {}
                valeurs_par_date_type[date_str][facture['type_facture']] = facture.get('montant', 0)
        
        labels = list(facture_dict.keys())
        data = list(facture_dict.values())
        total_factures = sum(data)
        
        # Trier les dates et types pour l'affichage
        dates_uniques = sorted(list(dates_uniques))
        types_facture = sorted(list(types_facture))
    else:
        labels = []
        data = []
        dates_uniques = []
        types_facture = []

    # Debug output
    print("Labels:", labels)
    print("Data:", data)
    print("Types Facture:", types_facture)
    print("Dates Uniques:", dates_uniques)
    print("Valeurs par Date/Type:", valeurs_par_date_type)

    return templates.TemplateResponse("conso.html", {
        "request": request,
        "labels": labels,
        "data": data,
        "total_factures": total_factures,
        "logements": logements,
        "selected_logement": selected_id,
        "has_factures": bool(factures),
        "types_facture": types_facture,
        "dates_uniques": dates_uniques,
        "valeurs_par_date_type": valeurs_par_date_type,
        "zip": zip
    })

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
async def add_facture(
    type_facture: str = Form(...),
    montant: float = Form(...),
    valeur_conso: float = Form(...),
    date_fact: str = Form(...),
    id_loge: str = Form(...)
):
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO Facture (type_facture, montant, valeur_conso, date_fact, id_loge)
            VALUES (?, ?, ?, ?, ?)
        """, (type_facture, montant, valeur_conso, date_fact, id_loge))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return RedirectResponse(url="/consommation", status_code=303)

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

@app.post("/supprimer_actionneur")
async def supprimer_capteur(actionneur: str = Form(...)):
    print(f"Suppression de l'actionneur avec id: {actionneur}")
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM Actionneur WHERE id_actionneur = ?", (actionneur,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

@app.post("/supprimer_type_capteur")
async def supprimer_type_capteur(type_capteur: str = Form(...)):
    print(f"Suppression du type de capteur avec id: {type_capteur}")
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM Type_capteur WHERE id_type = ?", (type_capteur,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return RedirectResponse(url="/config", status_code=303)

@app.get("/get_mesures")
async def get_mesures(capteur_id: int):
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT m.valeur, m.date_insert, t.unite_mesure
        FROM Mesure m
        JOIN Capteur c ON m.id_capteur = c.id_capteur
        JOIN Type_capteur t ON c.id_type = t.id_type
        WHERE m.id_capteur = ?
        ORDER BY m.date_insert
    """, (capteur_id,))
    rows = c.fetchall()
    conn.close()
    dates = [row['date_insert'] for row in rows]
    valeurs = [row['valeur'] for row in rows]
    unite_mesure = rows[0]['unite_mesure'] if rows else ''
    return {"dates": dates, "valeurs": valeurs, "unite_mesure": unite_mesure}

@app.post("/get-led_state")
async def set_led_state(request: Request):
    data = await request.json()
    actionneur_id = data.get("actionneur_id")
    led_state = data.get("led_state")

    return JSONResponse(content={"message": "LED state updated successfully", "actionneur_id": actionneur_id, "led_state": led_state})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

    #bash : uvicorn main:app --reload --host 127.0.0.1 --port 8000 ou fastapi run main.py