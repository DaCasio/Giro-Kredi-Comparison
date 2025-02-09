Giro-Kredi-Comparison
Dieses Projekt vergleicht den aktuellen Stand eines Girokontos – extrahiert aus einem öffentlichen Google Sheet – mit der taggenauen Restschuld eines Darlehens, die mit Hilfe von Python berechnet wird. Das Ergebnis wird als JSON-Datei (lametric.json) ausgegeben, die beispielsweise in einer LaMetric-MyData-App angezeigt werden kann.
Projektstruktur

    update_loan.py
    Berechnet die tägliche Restschuld des Darlehens. Es werden Startdatum, Darlehenskapital, Monatsrate und Zinssatz verwendet. Die Ergebnisstruktur wird auch in einer JSON-Datei namens darlehen.json abgelegt.
    extract_data.py
    Lädt das Google Sheet (im CSV-Format) aus dem Tab „dat“ (via URL mit Parameter &gid=0) und extrahiert aus Zeile 1 die Monatsnamen sowie aus Zeile 2 die zugehörigen Kontostände.
    Dabei werden Tausendertrennzeichen entfernt und das Dezimaltrennzeichen (Komma) in einen Punkt umgewandelt, sodass die Werte als Floats interpretiert werden.
    compare_balances.py
    Liest die aktuellen Daten aus dem Google Sheet (über extract_data.py) und berechnet die aktuelle Restschuld (über update_loan.py). Anschließend durchläuft es die Liste der extrahierten Kontostände und ermittelt den ersten Monat, in dem der Kontostand die Restschuld übersteigt. Das Ergebnis wird als JSON (lametric.json) ausgegeben.
    .github/workflows/update.yml
    Ein GitHub Actions-Workflow, der täglich (und per manueller Auslösung) ausgeführt wird. Er führt update_loan.py und compare_balances.py aus, aktualisiert lametric.json und commitet ggf. die Änderung zurück in das Repository.
    requirements.txt
    Listet die Python-Pakete (z. B. numpy und pandas) mit festgelegten Versionen auf, die für das Projekt benötigt werden.

Voraussetzungen

    Python 3.10 oder höher
    Abhängigkeiten gemäß requirements.txt (numpy==1.26.4, pandas==2.0.3)
    Ein öffentlich zugängliches Google Sheet mit zwei relevanten Zeilen:
        Zeile 1 (A1 bis BO1): Enthält die Monatsnamen (z. B. "Jun25,Jul25,...").
        Zeile 2 (A2 bis BO2): Enthält die zugehörigen Kontostände als Zahlen (mit Tausendertrennzeichen und Dezimal-Komma im deutschen Format).
    Ein LaMetric-Display oder eine MyData-App, die JSON-Daten von GitHub abrufen kann.

Funktionsweise

    Datenextraktion:
    Mit extract_data.py wird der CSV-Export des Google Sheets aus dem Tab „dat“ (URL:
    https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv&gid=0) geladen.
        Die erste Zeile wird anhand von Kommas in eine Liste von Monatsnamen zerlegt.
        Die zweite Zeile wird ebenfalls anhand von Kommas getrennt, wobei jedes Element bereinigt (Tausenderpunkte entfernen, Dezimalkomma in einen Punkt umwandeln) und in einen Float konvertiert wird.
    Darlehensberechnung:
    Das Skript update_loan.py berechnet anhand definierter Parameter (Startkapital, Monatsrate, Zinssatz etc.) die tägliche Weiterentwicklung der Restschuld bis zum aktuellen Datum.
    Vergleich:
    Mit compare_balances.py wird die Restschuld (z. B. 26122) mit den aus dem Google Sheet extrahierten Kontoständen verglichen. Der erste Monat, in dem der extrahierte Kontostand die Restschuld übersteigt, wird ermittelt und als Ergebnis (z. B. "Mär27") ausgegeben.
    JSON-Ausgabe:
    Das Ergebnis wird in einer JSON-Struktur abgelegt:

    json
    {
      "frames": [
        {
          "text": "Kontoüberhang: Mär27",
          "icon": "i17911"
        }
      ]
    }

    Automatisierung via GitHub Actions:
    Der Workflow (.github/workflows/update.yml) führt täglich die Aktualisierung durch, sodass die JSON-Datei immer den aktuell ermittelten Monat anzeigt.

Installation & Nutzung

    Repository klonen:

bash
git clone https://github.com/DaCasio/Giro-Kredi-Comparison.git
cd Giro-Kredi-Comparison

Abhängigkeiten installieren:

bash
pip install -r requirements.txt

Lokale Ausführung zur Überprüfung:

    bash
    python update_loan.py
    python compare_balances.py
    cat lametric.json

    GitHub Actions:
    Der Workflow wird automatisch täglich um 06:00 UTC (und bei manueller Auslösung) ausgeführt. Die erzeugte lametric.json kann direkt von der LaMetric MyData-App oder einem anderen Client abgerufen werden.

Anpassungen & Hinweise

    Google Sheet Formatierung:
    Achten Sie darauf, dass im Google Sheet die Werte in einem einzigen Tab (z. B. dem Tab „dat“) hinterlegt sind. Beim Export liegen dann alle Monatsnamen und entsprechenden Werte in der ersten Spalte, getrennt durch Kommas.
    Zahlenformat:
    Bei der Verarbeitung werden Tausendertrennzeichen entfernt und das Komma als Dezimaltrennzeichen umgewandelt. Falls andere Formate vorliegen, passen Sie den Code in extract_data.py gegebenenfalls an.
    Debugging:
    Bei Problemen wurden Debug-Ausgaben in den Skripten eingebaut, die über die GitHub Actions-Logs eingesehen werden können.

Lizenz
Dieses Projekt wird unter der MIT-Lizenz bereitgestellt. Details finden Sie in der LICENSE-Datei. Diese README.md fasst den aktuellen Stand des Projekts und dessen Funktionsweise zusammen. Nutzen Sie die Anweisungen, um das Projekt zu installieren, anzupassen und bei Bedarf zu erweitern.
