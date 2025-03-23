# Basis-Image mit Python
FROM python:3.9-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere requirements.txt zuerst, um Caching zu nutzen
COPY requirements.txt .

# Installiere die Abhängigkeiten
RUN pip install -r requirements.txt

# Kopiere den gesamten Code ins Arbeitsverzeichnis
COPY . .

# Installiere das Paket im Development-Modus
RUN pip install -e .

# Exponiere den Port für die Dash-App
EXPOSE 8050

# Starte die Dash-App
CMD ["python", "scripts/run_app.py", "--host", "0.0.0.0"]