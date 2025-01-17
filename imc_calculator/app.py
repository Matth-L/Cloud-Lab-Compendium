from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    """
    Init la base de données SQLite

    Elle sera sous la forme 
    (id(primary key), poids, taille_cm, imc)
    """
    conn = sqlite3.connect('imc_results.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poids REAL,
            taille_cm REAL,
            imc REAL
        )
    ''')

    conn.commit()
    conn.close()

def insert_result(poids, taille_cm, imc):
    """
    Insère une ligne dans la base de données
    """

    conn = sqlite3.connect('imc_results.db')
    cursor = conn.cursor()
    
    #insertion du résultat
    cursor.execute('INSERT INTO results (poids, taille_cm, imc) VALUES (?, ?, ?)'
                   , (poids, taille_cm, imc))
    
    conn.commit()
    conn.close()

def get_all_results():
    """
    Fais un SELECT * sur la table results et retourne le résultat
    """

    conn = sqlite3.connect('imc_results.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM results')
    results = cursor.fetchall()
    conn.close()
    return results

def calculer_imc(poids, taille_cm):
    """
    Effectue le calcul de l'imc

    @param poids: Poids en kilogrammes
    @param taille_cm: Taille en centimètres
    @return: IMC arrondi
    """
    taille_m = taille_cm / 100 
    return round(poids / (taille_m ** 2), 2)

@app.route('/', methods=['GET', 'POST'])
def accueil():
    if request.method == 'POST':
        poids = float(request.form.get('weight'))
        taille_cm = float(request.form.get('height'))
        imc = calculer_imc(poids, taille_cm)
        insert_result(poids, taille_cm, imc)
        return redirect(f'/resultat?imc={imc}')
    return render_template('index.html')

@app.route('/resultat')
def resultat():
    imc = request.args.get('imc')
    return render_template('result.html', imc=imc)

@app.route('/log')
def log():
    results = get_all_results()
    return render_template('log.html', results=results)

if __name__ == '__main__':
    # initialisation de la base de données avant de lancer l'application
    init_db()
    app.run(host='0.0.0.0', port=5000)
