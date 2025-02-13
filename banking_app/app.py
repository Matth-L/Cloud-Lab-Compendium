from flask import Flask, request, render_template
import sqlite3
from enum import Enum
import os 

app = Flask(__name__)

class Compte(Enum):
    """
    Structure nous permettant de déterminer les différentes valeurs possibles
    """
    COMPTE_EXISTE_DEJA = "Le compte existe déjà."
    COMPTE_NON_TROUVE = "Compte introuvable."
    VALEUR_INCORRECTE = "Valeur incorrecte."
    FONDS_INSUFFISANTS = "Fonds insuffisants."
    OK = "Opération effectuée avec succès."

DB_PATH = os.path.join(os.getcwd(), 'data.db')

def init_db():
    """
    Initialise la base de données banque.db
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comptes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE,
            solde REAL DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    

def existe_compte(nom:str) -> bool:
    """
    Vérifie si un compte existe déjà.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comptes WHERE nom = ?', (nom,))
    compte = cursor.fetchone()
    conn.close()
    return compte is not None

def creer_compte(nom : str) -> Compte:
    """
    Crée un compte, par défaut, le montant est à 0
    :param nom: nom du compte
    :return: Compte -> OK si le compte a été créé, sinon le code d'erreur
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ret = None

    if existe_compte(nom):
        ret = Compte.COMPTE_EXISTE_DEJA
    try:
        cursor.execute('INSERT INTO comptes (nom) VALUES (?)', (nom,))
        conn.commit()
        ret = Compte.OK
    except sqlite3.IntegrityError:
        return Compte.VALEUR_INCORRECTE
    
    conn.close()
    return ret
    
def effacer_compte(nom:str) -> Compte:
    """
    Supprime un compte de la base de données. 
    Si le compte n'existe pas, ne fait rien.
    """
    
    if not existe_compte(nom):
        return Compte.COMPTE_NON_TROUVE

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comptes WHERE nom = ?', (nom,))
    conn.commit()
    conn.close()
    return Compte.OK

def deposer_argent(nom:str, montant:float) -> Compte:
    """
    Dépose un montant sur un compte.
    """
    if montant <= 0:
        return Compte.VALEUR_INCORRECTE
    
    if not existe_compte(nom):
        return Compte.COMPTE_NON_TROUVE

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE comptes SET solde = solde + ? WHERE nom = ?', (montant, nom))
    conn.commit()
    conn.close()
    return Compte.OK

def retirer_argent(nom:str, montant:float) -> Compte:
    """
    Retire un montant du compte si le solde est suffisant.
    """

    if montant <= 0:
        return Compte.VALEUR_INCORRECTE

    if not existe_compte(nom):
        return Compte.COMPTE_NON_TROUVE

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT solde FROM comptes WHERE nom = ?', (nom,))
    compte = cursor.fetchone()
    ret = None

    if compte[0] >= montant:
        cursor.execute('UPDATE comptes SET solde = solde - ? WHERE nom = ?', (montant, nom))
        conn.commit()
        ret = Compte.OK
    else:
        ret = Compte.FONDS_INSUFFISANTS

    conn.close()
    return ret

def consulter_compte(nom:str) -> float:
    """
    Récupère le solde du compte spécifié.
    """
    conn = sqlite3.connect(DB_PATH)

    if not existe_compte(nom):
        return None

    cursor = conn.cursor()
    cursor.execute('SELECT solde FROM comptes WHERE nom = ?', (nom,))
    compte = cursor.fetchone()

    conn.close()
    return compte[0]

@app.route('/')
def accueil():
    """
    Page d'accueil.
    """
    return render_template('accueil.html')

@app.route('/creer_compte', methods=['GET', 'POST'])
def creer_compte_route():
    message = ""

    if request.method == 'POST':

        nom = request.form.get('nom')
        message = creer_compte(nom).value

    return render_template('creer_compte.html', message=message)

@app.route('/effacer_compte', methods=['GET', 'POST'])
def effacer_compte_route():
    message = ""

    if request.method == 'POST':

        nom = request.form.get('nom')
        message = effacer_compte(nom).value

    return render_template('effacer_compte.html', message=message)

@app.route('/deposer', methods=['GET', 'POST'])
def deposer_route():
    message = ""

    if request.method == 'POST':

        nom = request.form.get('nom')
        montant = request.form.get('montant')
        message = deposer_argent(nom, float(montant)).value

    return render_template('deposer.html', message=message)

@app.route('/retirer', methods=['GET', 'POST'])
def retirer_route():
    message = ""
    
    if request.method == 'POST':

        nom = request.form.get('nom')
        montant = request.form.get('montant')
        message = retirer_argent(nom, float(montant)).value

    return render_template('retirer.html', message=message)

@app.route('/consulter', methods=['GET', 'POST'])
def consulter_route():
    message = ""
    if request.method == 'POST':
        nom = request.form.get('nom')
        solde = consulter_compte(nom)
        if solde is None:
            message = Compte.COMPTE_NON_TROUVE.value
        else:
            message = f"Solde du compte {nom}: {solde} €"
    return render_template('consulter.html', message=message)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
