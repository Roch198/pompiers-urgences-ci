from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash, session
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from PIL import Image
import database
from config import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = SECRET_KEY
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'info'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.password_hash = user_data['password_hash']
        self.role = user_data['role']
        self.telephone = user_data['telephone']

@login_manager.user_loader
def load_user(user_id):
    user_data = database.get_user_by_id(int(user_id))
    return User(user_data) if user_data else None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'pompier')
        telephone = request.form.get('telephone')
        
        # Vérifier le mot de passe pour les pompiers
        if role == 'pompier' and password != POMPIER_PASSWORD:
            flash('Mot de passe incorrect pour les pompiers', 'danger')
            return redirect(url_for('register'))
        
        # Créer un nouvel utilisateur
        success = database.create_user(
            username=username,
            password_hash=generate_password_hash(POMPIER_PASSWORD if role == 'pompier' else password),
            role=role,
            telephone=telephone
        )
        
        if success:
            flash('Inscription réussie ! Vous pouvez maintenant vous connecter', 'success')
            return redirect(url_for('login'))
        else:
            flash('Nom d\'utilisateur déjà pris', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = database.get_user_by_username(username)
        if user_data:
            # Vérifier le mot de passe en fonction du rôle
            correct_password = (
                password == POMPIER_PASSWORD if user_data['role'] == 'pompier'
                else check_password_hash(user_data['password_hash'], password)
            )
            
            if correct_password:
                user = User(user_data)
                login_user(user)
                flash('Connexion réussie !', 'success')
                return redirect(url_for('dashboard'))
        
        flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('welcome'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/urgences', methods=['POST'])
@login_required
def creer_urgence():
    try:
        # Gérer les données du formulaire
        type_urgence = request.form.get('type')
        commune = request.form.get('commune')
        adresse = request.form.get('adresse')
        description = request.form.get('description')
        nb_personnes = request.form.get('personnes')
        
        # Gérer la photo
        photo_filename = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                # Générer un nom de fichier unique
                filename = secure_filename(photo.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                photo_filename = timestamp + filename
                
                # Redimensionner et sauvegarder l'image
                img = Image.open(photo)
                img.thumbnail((800, 800))  # Redimensionner à max 800x800
                img.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        # Créer l'urgence dans la base de données
        database.create_urgence(
            type_urgence=type_urgence,
            commune=commune,
            adresse=adresse,
            description=description,
            nb_personnes=int(nb_personnes),
            photo=f'/uploads/{photo_filename}' if photo_filename else None
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/urgences', methods=['GET'])
@login_required
def liste_urgences():
    urgences = database.get_all_urgences()
    return jsonify(urgences)

@app.route('/api/urgences/<int:urgence_id>/terminer', methods=['POST'])
@login_required
def terminer_urgence(urgence_id):
    try:
        # Vérifier si l'utilisateur est un pompier
        if current_user.role != 'pompier':
            return jsonify({'success': False, 'error': 'Accès non autorisé. Seuls les pompiers peuvent terminer une intervention.'}), 403
            
        database.update_urgence_status(urgence_id, 'Terminé')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/urgences/<int:urgence_id>/supprimer', methods=['POST'])
@login_required
def supprimer_urgence(urgence_id):
    try:
        # Vérifier si l'utilisateur est un pompier
        if current_user.role != 'pompier':
            return jsonify({'success': False, 'error': 'Accès non autorisé. Seuls les pompiers peuvent supprimer une intervention.'}), 403
            
        if database.delete_urgence(urgence_id):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Erreur lors de la suppression'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    # Initialiser la base de données au démarrage
    database.init_db()
    # Créer le dossier uploads s'il n'existe pas
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(port=8080, debug=True)
