import sqlite3
from .contravention import Contravention

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/db.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def rechercher_contraventions(self, valeur):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM contraventions WHERE etablissement LIKE ? OR proprietaire LIKE ? OR adresse LIKE ?"
                       ,(f"%{valeur}%", f"%{valeur}%", f"%{valeur}%"))
        toutes_contrav = cursor.fetchall()
        return [Contravention(id_poursuite=contrav[0],
                business_id=contrav[1],
                date=contrav[2],
                description=contrav[3],
                adresse=contrav[4],
                date_jugement=contrav[5],
                etablissement=contrav[6],
                montant=contrav[7],
                proprietaire=contrav[8],
                ville=contrav[9],
                statut=contrav[10],
                date_statut=contrav[11],
                categorie=contrav[12]) 
                for contrav in toutes_contrav]
    
    def rechercher_entre_deux_dates(self, date_debut, date_fin):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM contraventions WHERE date BETWEEN ? AND ?", (date_debut, date_fin))
        toutes_contrav = cursor.fetchall()
        return [Contravention(id_poursuite=contrav[0],
                business_id=contrav[1],
                date=contrav[2],
                description=contrav[3],
                adresse=contrav[4],
                date_jugement=contrav[5],
                etablissement=contrav[6],
                montant=contrav[7],
                proprietaire=contrav[8],
                ville=contrav[9],
                statut=contrav[10],
                date_statut=contrav[11],
                categorie=contrav[12]) 
                for contrav in toutes_contrav]

    def rechercher_date_etablissement(self, date_debut, date_fin):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT DISTINCT etablissement FROM contraventions WHERE date BETWEEN ? AND ?",
            (date_debut, date_fin)
        )
        toutes_contrav = cursor.fetchall()
        return [contrav[0] for contrav in toutes_contrav]
    
    def liste_contrevenants(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT etablissement, "
        "COUNT(*) AS nombre_contrav "
        "FROM contraventions "
        "WHERE etablissement IS NOT NULL "
        "GROUP BY etablissement "
        "ORDER BY nombre_contrav DESC")
        toutes_contrav = cursor.fetchall()
        return [{"etablissement": contrav[0], 
                 "nombre_contrav": contrav[1]} 
                 for contrav in toutes_contrav]
    
    # def liste_etablissements (self):
    #     cursor = self.get_connection().cursor()
    #     cursor.execute("SELECT DISTINCT etablissement FROM contraventions")
    #     toutes_contrav = cursor.fetchall()
    #     return [contrav[0] for contrav in toutes_contrav]
        
    def rechercher_entre_deux_dates_et_etablissement (self,date_debut,date_fin, etablissement):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM contraventions WHERE etablissement LIKE ? AND date BETWEEN ? AND ? ", (etablissement, date_debut, date_fin))
        toutes_contrav = cursor.fetchall()
        return [Contravention(id_poursuite=contrav[0],
                business_id=contrav[1],
                date=contrav[2],
                description=contrav[3],
                adresse=contrav[4],
                date_jugement=contrav[5],
                etablissement=contrav[6],
                montant=contrav[7],
                proprietaire=contrav[8],
                ville=contrav[9],
                statut=contrav[10],
                date_statut=contrav[11],
                categorie=contrav[12]) 
                for contrav in toutes_contrav]