# Basis-Image mit Python
FROM python:3.11.4

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere requirements.txt zuerst, um Caching zu nutzen
COPY requirements.txt /app/

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Code ins Arbeitsverzeichnis
COPY . /app/

# Setze den Arbeitsordner auf das Verzeichnis mit der Dash-App
WORKDIR /app/text_cluster

# Exponiere den Port für die Dash-App (falls erforderlich)
EXPOSE 8050

# Starte die Dash-App (ändere "run.py" falls nötig)
CMD ["python", "run_d.py"]