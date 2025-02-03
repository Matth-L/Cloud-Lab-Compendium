# Importation des modules nécessaires
from flask import Flask, request, redirect, render_template
import sqlite3

# Initialisation de l'application Flask
app = Flask(__name__)

def init_db():
    """
    Initialise la base de données SQLite.

    La table sera sous la forme :
    (id (primary key), poids, taille_cm, imc)
    """
    conn = sqlite3.connect('imc_results.db')  # Connexion à la base de données SQLite
    cursor = conn.cursor()  # Création d'un curseur pour exécuter des commandes SQL

    # Création de la table si elle n'existe pas déjà
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poids REAL,
            taille_cm REAL,
            imc REAL
        )
    ''')

    conn.commit()  # Validation des changements
    conn.close()  # Fermeture de la connexion

def insert_result(poids, taille_cm, imc):
    """
    Insère une ligne dans la base de données.

    @param poids: Poids en kilogrammes
    @param taille_cm: Taille en centimètres
    @param imc: Indice de Masse Corporelle calculé
    """
    conn = sqlite3.connect('imc_results.db')  # Connexion à la base de données SQLite
    cursor = conn.cursor()  # Création d'un curseur pour exécuter des commandes SQL
    
    # Insertion du résultat
    cursor.execute('INSERT INTO results (poids, taille_cm, imc) VALUES (?, ?, ?)', (poids, taille_cm, imc))
    
    conn.commit()  # Validation des changements
    conn.close()  # Fermeture de la connexion

def get_all_results():
    """
    Effectue un SELECT * sur la table results et retourne le résultat.

    @return: Liste des résultats de la table
    """
    conn = sqlite3.connect('imc_results.db')  # Connexion à la base de données SQLite
    cursor = conn.cursor()  # Création d'un curseur pour exécuter des commandes SQL
    cursor.execute('SELECT * FROM results')  # Exécution de la requête SQL
    results = cursor.fetchall()  # Récupération de tous les résultats
    conn.close()  # Fermeture de la connexion
    return results  # Retourne les résultats

def calculer_imc(poids, taille_cm):
    """
    Effectue le calcul de l'IMC.

    @param poids: Poids en kilogrammes
    @param taille_cm: Taille en centimètres
    @return: IMC arrondi
    """
    taille_m = taille_cm / 100  # Conversion de la taille en mètres
    return round(poids / (taille_m ** 2), 2)  # Calcul de l'IMC et arrondi à 2 décimales

@app.route('/', methods=['GET', 'POST'])
def accueil():
    """
    Route pour la page d'accueil.

    Si la méthode est POST, calcule l'IMC et insère le résultat dans la base de données,
    puis redirige vers la page de résultat. Sinon, affiche la page d'accueil.
    """
    if request.method == 'POST':
        poids = float(request.form.get('weight'))  # Récupération du poids depuis le formulaire
        taille_cm = float(request.form.get('height'))  # Récupération de la taille depuis le formulaire
        imc = calculer_imc(poids, taille_cm)  # Calcul de l'IMC
        insert_result(poids, taille_cm, imc)  # Insertion du résultat dans la base de données
        return redirect(f'/resultat?imc={imc}')  # Redirection vers la page de résultat avec l'IMC en paramètre
    return render_template('index.html')  # Affichage de la page d'accueil

@app.route('/resultat')
def resultat():
    """
    Route pour la page de résultat.

    Affiche l'IMC calculé.
    """
    imc = request.args.get('imc')  # Récupération de l'IMC depuis les paramètres de la requête
    return render_template('result.html', imc=imc)  # Affichage de la page de résultat avec l'IMC

@app.route('/log')
def log():
    """
    Route pour la page de log.

    Affiche tous les résultats enregistrés dans la base de données.
    """
    results = get_all_results()  # Récupération de tous les résultats depuis la base de données
    return render_template('log.html', results=results)  # Affichage de la page de log avec les résultats

if __name__ == '__main__':
    # Initialisation de la base de données avant de lancer l'application
    init_db()
    app.run(host='0.0.0.0', port=5000)  # Lancement de l'application Flask