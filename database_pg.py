import os
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from werkzeug.security import generate_password_hash
from config import POMPIER_PASSWORD

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    
    # Créer la table users
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            telephone TEXT NOT NULL
        )
    ''')
    
    # Créer la table urgences
    cur.execute('''
        CREATE TABLE IF NOT EXISTS urgences (
            id SERIAL PRIMARY KEY,
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
        cur.execute('''
            INSERT INTO users (username, password_hash, role, telephone)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
        ''', ('pompier1', generate_password_hash(POMPIER_PASSWORD), 'pompier', '0123456789'))
    except Exception as e:
        print(f"Erreur lors de la création du compte pompier par défaut : {e}")
    
    cur.close()
    conn.close()

def create_user(username, password_hash, role, telephone):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO users (username, password_hash, role, telephone) VALUES (%s, %s, %s, %s)',
            (username, password_hash, role, telephone)
        )
        return True
    except psycopg2.IntegrityError:
        return False
    finally:
        cur.close()
        conn.close()

def get_user_by_username(username):
    conn = get_db()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return dict(user) if user else None

def create_urgence(type_urgence, commune, adresse, description, nb_personnes, photo=None):
    conn = get_db()
    cur = conn.cursor()
    date_creation = datetime.now().strftime('%d/%m/%Y %H:%M')
    cur.execute(
        '''INSERT INTO urgences 
           (type_urgence, commune, adresse, description, nb_personnes, date_creation, statut, photo)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
        (type_urgence, commune, adresse, description, nb_personnes, date_creation, 'En cours', photo)
    )
    cur.close()
    conn.close()

def get_all_urgences():
    conn = get_db()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * FROM urgences ORDER BY id DESC')
    urgences = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(urgence) for urgence in urgences]

def update_urgence_status(urgence_id, nouveau_statut):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'UPDATE urgences SET statut = %s WHERE id = %s',
        (nouveau_statut, urgence_id)
    )
    cur.close()
    conn.close()

def delete_urgence(urgence_id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM urgences WHERE id = %s', (urgence_id,))
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression de l'urgence: {e}")
        return False
    finally:
        cur.close()
        conn.close()
