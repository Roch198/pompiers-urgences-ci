import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH, POMPIER_PASSWORD
from werkzeug.security import generate_password_hash

# Utiliser le chemin de la base de données depuis la configuration
DB_FILE = DATABASE_PATH

def init_db():
    # Assurer que le dossier parent existe
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Créer la table users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            telephone TEXT NOT NULL
        )
    ''')
    
    # Créer la table urgences
    c.execute('''
        CREATE TABLE IF NOT EXISTS urgences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_urgence TEXT NOT NULL,
            commune TEXT NOT NULL,
            adresse TEXT NOT NULL,
            description TEXT NOT NULL,
            nb_personnes INTEGER NOT NULL,
            date_creation TEXT NOT NULL,
            statut TEXT NOT NULL,
            photo TEXT
        )
    ''')
    
    # Créer un compte pompier par défaut s'il n'existe pas
    try:
        c.execute('INSERT OR IGNORE INTO users (username, password_hash, role, telephone) VALUES (?, ?, ?, ?)',
                 ('pompier1', generate_password_hash(POMPIER_PASSWORD), 'pompier', '0123456789'))
    except Exception as e:
        print(f"Erreur lors de la création du compte pompier par défaut : {e}")
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn

# Fonctions pour les utilisateurs
def create_user(username, password_hash, role, telephone):
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, password_hash, role, telephone) VALUES (?, ?, ?, ?)',
            (username, password_hash, role, telephone)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_username(username):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

# Fonctions pour les urgences
def create_urgence(type_urgence, commune, adresse, description, nb_personnes, photo=None):
    conn = get_db()
    date_creation = datetime.now().strftime('%d/%m/%Y %H:%M')
    conn.execute(
        '''INSERT INTO urgences 
           (type_urgence, commune, adresse, description, nb_personnes, date_creation, statut, photo)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (type_urgence, commune, adresse, description, nb_personnes, date_creation, 'En cours', photo)
    )
    conn.commit()
    conn.close()

def get_all_urgences():
    conn = get_db()
    urgences = conn.execute('SELECT * FROM urgences ORDER BY id DESC').fetchall()
    conn.close()
    return [dict(urgence) for urgence in urgences]

def update_urgence_status(urgence_id, nouveau_statut):
    conn = get_db()
    conn.execute(
        'UPDATE urgences SET statut = ? WHERE id = ?',
        (nouveau_statut, urgence_id)
    )
    conn.commit()
    conn.close()

def delete_urgence(urgence_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM urgences WHERE id = ?', (urgence_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression de l'urgence: {e}")
        return False
    finally:
        cursor.close()
