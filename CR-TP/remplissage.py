import sqlite3, random

# ouverture/initialisation de la base de donnee 
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


id_capteur = 1

# Insertion de 5 mesures 
mesures = [
(23.5, '2024-11-01'),  # Valeur : 23.5, Date : 1 novembre 2024
(45.2, '2024-11-02'),  
(67.8, '2024-11-03'),  
(12.3, '2024-11-04'),  
(98.7, '2024-11-05')   
]

for valeur, date_insert in mesures:
    query = '''INSERT INTO Mesure (valeur, date_insert, id_capteur)
            VALUES (?, ?, ?)'''
    c.execute(query, (valeur, date_insert, id_capteur))

    id_loge = 1

    # Insertion de 4 factures avec des valeurs fixes et des dates cohérentes
    factures = [
        ('Électricité', 120.50, 350.5, '2024-11-01'),  # Électricité : 120.50€, Consommation : 350.5 kWh
        ('Eau', 45.75, 150.3, '2024-11-02'),          # Eau : 45.75€, Consommation : 150.3 m³
        ('Chauffage', 90.00, 210.0, '2024-11-03'),    # Chauffage : 90.00€, Consommation : 210.0 kWh
        ('Internet', 40.00, 0.0, '2024-11-04')       # Internet : 40.00€, Pas de consommation
    ]
    
    for type_facture, montant, valeur_conso, date_fact in factures:
        query = '''INSERT INTO Facture (type_facture, montant, valeur_conso, date_fact, id_loge)
                   VALUES (?, ?, ?, ?, ?)'''
        c.execute(query, (type_facture, montant, valeur_conso, date_fact, id_loge))



# fermeture
conn.commit()
conn.close()