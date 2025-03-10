import os

# Obtenir le chemin absolu du répertoire de l'application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configuration de l'application
SECRET_KEY = os.environ.get('SECRET_KEY', 'votre_clé_secrète_ici')
UPLOAD_FOLDER = os.path.abspath(os.environ.get('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads')))
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max

# Configuration des pompiers
POMPIER_PASSWORD = os.environ.get('POMPIER_PASSWORD', 'Pompier2025!')

# Configuration de la base de données
DATABASE_PATH = os.path.abspath(os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'instance', 'pompiers.db')))

# Extensions autorisées pour les images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
