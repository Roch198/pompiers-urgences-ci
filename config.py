import os

# Configuration de l'application
SECRET_KEY = os.environ.get('SECRET_KEY', 'votre_clé_secrète_ici')
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max

# Configuration des pompiers
POMPIER_PASSWORD = os.environ.get('POMPIER_PASSWORD', 'Pompier2025!')

# Configuration de la base de données
DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join('instance', 'pompiers.db'))

# Extensions autorisées pour les images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
