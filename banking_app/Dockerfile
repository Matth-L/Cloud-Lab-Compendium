FROM python:3.11-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers nécessaires dans l'image
COPY requirements.txt .
COPY app.py .
COPY templates/ templates/

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposition du port 5000
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python", "app.py"]
