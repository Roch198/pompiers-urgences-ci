import os

# Configuration de l'application
SECRET_KEY = 'votre_clé_secrète_ici'
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max

# Configuration des pompiers
POMPIER_PASSWORD = 'Pompier2025!'  # Mot de passe unique pour tous les pompiers
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
