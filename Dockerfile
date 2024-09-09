# Verwende ein Python 3.9 Image
FROM python:3.9-slim

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere die requirements.txt und installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kopiere den Rest der App
COPY . .

# Setze Umgebungsvariablen für Flask
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Exponiere Port 5000
EXPOSE 5000

# Starte die Flask App
CMD ["flask", "run", "--host=0.0.0.0"]
