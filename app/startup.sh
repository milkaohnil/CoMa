#!/bin/bash

echo "Starting script..."
echo "Check Connection to MariaDB..."

# Die Datenbank-Anmeldeinformationen aus den Umgebungsvariablen beziehen
DATABASE_USER=${MARIADB_USER}
DATABASE_PASSWORD=${MARIADB_PASSWORD}
DATABASE=${MARIADB_DB}
DATABASE_SERVER=${MARIADB_SERVER}

while :
do
  # Teste die Verbindung zur MariaDB, bis sie verfügbar ist
  db_available=$(mariadb -h "$DATABASE_SERVER" -u root --password="$DATABASE_PASSWORD" &> /dev/null && echo $?)
  if [ "$db_available" == 0 ]; then
    echo "MariaDB is reachable"
    break
  fi
  # Warte 5 Sekunden vor dem nächsten Verbindungsversuch
  echo "Waiting for MariaDB to become available..."
  sleep 5
done

# Setze die Datenbankverbindung als Umgebungsvariable
export DATABASE_URL="mysql+pymysql://root:${DATABASE_PASSWORD}@${DATABASE_SERVER}/${DATABASE}"

# Initialisiere die Datenbank, falls erforderlich
echo "Check if MariaDB has to be initialized..."
already_initialized=$(flask db show &> /dev/null && echo $?)
if [ "$already_initialized" != 0 ]; then
  echo "MariaDB has to be initialized..."
  flask db init
  flask db migrate -m "create tables"
  flask db upgrade
  echo "MariaDB initialized!"
else
  echo "MariaDB is already initialized"
fi

# Starte die Flask-Anwendung
echo "Starting up FLASK web application"
flask run -h 0.0.0.0
