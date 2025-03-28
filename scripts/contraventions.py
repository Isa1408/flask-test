import sqlite3
import time
import requests
import csv
from apscheduler.schedulers.background import BackgroundScheduler

bd = "../db/db.db"
table = "contraventions"
lien = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

def extraire_donnees():
    # Aller chercher les données à partir du lien
    # Si le statut n'est pas 200 alors on lève une exception
    data = requests.get(lien)
    if data.status_code != 200:
        raise Exception(f"Une erreur s'est produite. Statut : {data.status_code}")

    data = data.content.decode("utf-8")
    une_data = csv.reader(data.splitlines())
    # La première ligne est les noms des colonnes
    premiere_ligne = next(une_data)
    reste_lignes = list(une_data)

    # Connexion et insertion des données dans la table
    connexion = sqlite3.connect(bd)
    curseur = connexion.cursor()
    inserer_donees = f"""
    INSERT OR IGNORE INTO {table} (
        id_poursuite, business_id, date, description, adresse, date_jugement,
        etablissement, montant, proprietaire, ville, statut, date_statut, categorie
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    curseur.executemany(inserer_donees, reste_lignes)
    connexion.commit()
    connexion.close()

    print(f"Les données ont été ajouté dans la table.")

# Exécuter le script une fois lors de l'exécution du script
print("Exécution immédiate de l'extraction des données...")
extraire_donnees()

planif_arriere_plan = BackgroundScheduler()
planif_arriere_plan.add_job(extraire_donnees, 'cron', hour=0, minute=0)
planif_arriere_plan.start()
print("Les données seront extraites à chaque jour, à minuit.")

# Faire tourner en arrière plan
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    planif_arriere_plan.shutdown()
    print("Le planificateur d'arrière plan va maintenant s'arrêter.")