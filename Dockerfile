# Verwende ein Python 3.9 Image
FROM python:3.9-slim

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere die requirements.txt und installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install -r requirements.txt

# Installiere MariaDB-Client (oder mysql-client)
RUN apt-get update && apt-get install -y mariadb-client
RUN pip install Flask-Migrate

# Kopiere das startup.sh Skript ins Image
COPY startup.sh /app/startup.sh

# Mache das startup.sh Skript ausführbar
RUN chmod +x /app/startup.sh

# Kopiere den Rest der App
COPY . .

# Setze Umgebungsvariablen für Flask
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Exponiere Port 5000
EXPOSE 5000

# Starte die Flask App
CMD ["/bin/sh", "-c", "flask run --host=0.0.0.0"]
