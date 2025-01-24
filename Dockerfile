# Utiliser une image Python comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le contenu de votre projet dans le conteneur
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Exécuter le script d'initialisation de la base de données
RUN python init_db.py

# Exposer le port sur lequel l'application fonctionnera
EXPOSE 5000

# Démarrer l'application Flask
CMD ["python", "app.py"]
