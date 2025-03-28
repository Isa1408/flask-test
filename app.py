from datetime import datetime
from flask import Flask, Response, abort, jsonify, redirect, request, url_for
from flask import render_template
from flask import g
from .database import Database
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
import json
from xml.sax.saxutils import escape
import csv
from io import StringIO

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_url_path="/static", static_folder="static")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('erreur-404.html'), 404

@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400

# @app.route('/')
# def start_page():
#     try:
#         bd = get_db()
#         etablissements = bd.liste_etablissements()
#         return render_template('accueil.html', etablissements=etablissements)
#     except Exception as e:
#         return render_template('accueil.html', etablissements=[], error="Une erreur interne s'est produite.")
@app.route('/')
def start_page():
    return render_template('accueil.html')


# doit retourner une nouvelle page HTML
@app.route('/rechercher')
def rechercher():
    valeur = request.args.get('contraventions')

    try:
        bd = get_db()
        contraventions = bd.rechercher_contraventions(valeur)
        # jsp si j en ai besoin pcq cette route retourne une page HTML
        # if not contraventions:
        #     abort(404, description=f"Aucune contravention correspond aux critères de recherche.")
        return render_template('page_contraventions.html', contraventions=contraventions)
    except Exception as e:
        return jsonify(error="Une erreur interne s'est produite."), 500

# doit retourner un JSON
@app.route('/api/contrevenants', methods=['GET'])
def contrevenants():
    date_debut = request.args.get('du')
    date_fin = request.args.get('au')
    etablissement = request.args.get('etablissement-deroulant')

    if not date_debut or not date_fin:
        return jsonify(error="Les paramètres 'du' et 'au' sont requis et "
        "les dates doivent être au format YYYY-MM-DD ISO 8601."), 400

    # Vérifier si les dates sont en format YYYY-MM-DD ISO 8601 
    # et les convertir en format YYYYMMDD afin de les comparer 
    # avec les dates de la BD
    try:
        date_debut = datetime.strptime(date_debut, "%Y-%m-%d").strftime("%Y%m%d")
        date_fin = datetime.strptime(date_fin, "%Y-%m-%d").strftime("%Y%m%d")
    except ValueError:
        return jsonify(error="Les paramètres 'du' et 'au' sont requis et "
        "les dates doivent être au format YYYY-MM-DD ISO 8601."), 400

    # Vérifier s'il y a des contraventions entre les dates spécifiées 
    try:
        bd = get_db()
        # dans le cas où un établissement est spécifié
        if etablissement:
            contraventions = bd.rechercher_entre_deux_dates_et_etablissement(date_debut, date_fin, etablissement)
        else:
            contraventions = bd.rechercher_entre_deux_dates(date_debut, date_fin)
        if contraventions:
            return jsonify([contrav.asDictionary() for contrav in contraventions]), 200
        else:
            return jsonify(error="Aucune contravention correspond aux critères de recherche."), 404
    except Exception as e:
        return jsonify(error="Une erreur interne s'est produite."), 500

@app.route('/api/contrevenants.json', methods=['GET'])
def contrevenants_json():
    try :
        bd = get_db()
        contrevenants = bd.liste_contrevenants()

        # dans le cas où la bd est vide
        if not contrevenants:
            return jsonify(error="Aucun contravenant n'a été trouvé."), 404
        return jsonify(contrevenants), 200
    except Exception as e:
        return jsonify(error="Une erreur interne s'est produite."), 500

@app.route('/api/contrevenants.xml', methods=['GET'])
def contrevenants_xml():
    try:
        bd = get_db()
        contrevenants = bd.liste_contrevenants()

        # dans le cas où la bd est vide
        if not contrevenants:
            return Response(response="<error>Aucun contravenant n'a été trouvé.</error>", status=404, mimetype="application/xml")

        # créer le xml
        xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xml += '<contrevenants>'

        for contrav in contrevenants:
            xml += '<un_contrevenant>'
            # xml += f'<etablissement>{escape(contrav.get("etablissement", "vide"))}</etablissement>'
            # xml += f'<nbr_contrav>{escape(str(contrav.get("nombre_contrav", 0)))}</nbr_contrav>'
            xml += f'<etablissement>{escape(contrav.get("etablissement"))}</etablissement>'
            xml += f'<nbr_contrav>{escape(str(contrav.get("nombre_contrav")))}</nbr_contrav>'
            xml += '</un_contrevenant>'
            
        xml += '</contrevenants>'
        return Response(response=xml, status=200, mimetype="application/xml")

    except Exception as e:
        return Response(response="<error>Une erreur interne s'est produite.</error>", status=500, mimetype="application/xml")

@app.route('/api/contrevenants.csv', methods=['GET'])
def contrevenants_csv():
    try:
        bd = get_db()
        contrevenants = bd.liste_contrevenants()

        # dans le cas où la bd est vide
        if not contrevenants:
            return Response(response="Aucun contravenant n'a été trouvé.", status=404, mimetype="text/plain")

        sortie = StringIO()
        ecrire = csv.writer(sortie, quoting=csv.QUOTE_ALL)

        # On ecrit l'entete d'abord puis les donnees
        ecrire.writerow(["Etablissement", "Nombre d'infractions"])
        for contrav in contrevenants:
            # ecrire.writerow([contrav.get("etablissement", "vide"), contrav.get("nombre_contrav", 0)])
            ecrire.writerow([contrav["etablissement"], contrav["nombre_contrav"]])

        contenu = sortie.getvalue()
        sortie.close()
        retour = Response(contenu, mimetype="text/csv; charset=utf-8", status=200)
        retour.headers["Content-Disposition"] = "attachment; filename=contrevenants.csv"
        return retour

    except Exception as e:
        return Response(response="Une erreur interne s'est produite.", status=500, mimetype="text/plain")

# sert pour la liste déroulante des établissements
@app.route('/api/filtre_etablissements', methods=['GET'])
def etablissements():
    date_debut = request.args.get('du')
    date_fin = request.args.get('au')

    if not date_debut or not date_fin:
        return jsonify(error="Les paramètres 'du' et 'au' sont requis et "
        "les dates doivent être au format YYYY-MM-DD ISO 8601."), 400

    try:
        date_debut = datetime.strptime(date_debut, "%Y-%m-%d").strftime("%Y%m%d")
        date_fin = datetime.strptime(date_fin, "%Y-%m-%d").strftime("%Y%m%d")
    except ValueError:
        return jsonify(error="Les paramètres 'du' et 'au' sont requis et "
        "les dates doivent être au format YYYY-MM-DD ISO 8601."), 400

    try:
        bd = get_db()
        etablissements = bd.rechercher_date_etablissement(date_debut, date_fin)
        return jsonify(etablissements), 200
    except Exception as e:
        return jsonify(error="Une erreur interne s'est produite."), 500

@app.route('/doc')
def documentation():
    return render_template('doc.html')

if __name__ == '__main__':
    app.run(debug=True)