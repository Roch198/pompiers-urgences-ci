import sqlite3
import os
from datetime import datetime

DB_FILE = 'instance/pompiers.db'

def init_db():
    # Assurer que le dossier instance existe
    os.makedirs('instance', exist_ok=True)
    
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
