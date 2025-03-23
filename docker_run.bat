@echo off
echo Starte Text-Cluster-Comparison Docker-Container...
echo Docker-Desktop has to run
REM Starte den Container
echo Starte Container...
docker run -p 8050:8050 text-cluster-comparison
echo 127.0.0.1:8050
REM Bei Fehler
if %errorlevel% neq 0 (
    echo Fehler beim Starten des Containers.
    echo Mögliche Probleme:
    echo - Port 8050 wird bereits verwendet
    echo - Unzureichende Berechtigungen
    echo - Docker hat Probleme mit dem Image
    pause
)