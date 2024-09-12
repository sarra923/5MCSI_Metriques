from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)   
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

# Fonction pour extraire les minutes à partir d'une date au format ISO
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Nouvelle route pour afficher les commits sous forme de graphique
@app.route('/commits/')
def get_commits():
    # URL de l'API GitHub pour récupérer les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    # Récupérer les données de l'API
    response = urlopen(url)
    raw_data = response.read()
    json_data = json.loads(raw_data.decode('utf-8'))
    
    # Extraire les minutes des dates des commits
    commit_times = []
    for commit in json_data:
        commit_date = commit['commit']['author']['date']
        minutes = extract_minutes_from_date(commit_date)
        commit_times.append(minutes)

# Envoyer les minutes des commits à la page HTML
    return render_template("commits.html", commits=commit_times)

# Fonction pour extraire les minutes d'un timestamp donné
def extract_minutes_from_date(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute
  
if __name__ == "__main__":
  app.run(debug=True)
