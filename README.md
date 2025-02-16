# Giro-Kredi-Comparison

Dieses Projekt vergleicht den aktuellen Stand eines Girokontos – extrahiert aus einem öffentlichen Google Sheet – mit der taggenauen Restschuld eines Darlehens, die mit Hilfe von Python berechnet wird. Das Ergebnis wird als JSON-Datei (lametric.json) ausgegeben, die beispielsweise in einer LaMetric-MyData-App angezeigt werden kann.

## Projektstruktur

- **update_loan.py**  
  Berechnet die tägliche Restschuld des Darlehens. Es werden Startdatum, Darlehenskapital, Monatsrate und Zinssatz verwendet. Die Ergebnisstruktur wird auch in einer JSON-Datei namens `darlehen.json` abgelegt.

- **extract_data.py**  
  Lädt das Google Sheet (im CSV-Format) aus dem Tab „dat“ (via URL mit Parameter &gid=0) und extrahiert aus Zeile 1 die Monatsnamen sowie aus Zeile 2 die zugehörigen Kontostände. Dabei werden Tausendertrennzeichen entfernt und das Dezimaltrennzeichen (Komma) in einen Punkt umgewandelt, sodass die Werte als Floats interpretiert werden.

- **compare_balances.py**  
  Liest die aktuellen Daten aus dem Google Sheet (über `extract_data.py`) und berechnet die aktuelle Restschuld (über `update_loan.py`). Anschließend durchläuft es die Liste der extrahierten Kontostände und ermittelt den ersten Monat, in dem der Kontostand die Restschuld übersteigt. Zusätzlich wird für den ermittelten Zielmonat (z. B. "Mär27") die genaue Zeitspanne (in vollen Monaten und verbleibenden Tagen) bis zum Ereignis berechnet. Das Ergebnis wird als JSON (lametric.json) ausgegeben.

- **.github/workflows/update.yml**  
  Ein GitHub Actions-Workflow, der täglich (und per manueller Auslösung) ausgeführt wird. Er führt `update_loan.py` und `compare_balances.py` aus, aktualisiert `lametric.json` und committet ggf. die Änderung zurück in das Repository.

- **requirements.txt**  
  Listet die für das Projekt benötigten Python-Pakete auf.

## Voraussetzungen

- Python 3.10 oder höher
- Abhängigkeiten gemäß requirements.txt (pandas und numpy)
- Ein öffentlich zugängliches Google Sheet mit zwei relevanten Zeilen:
  - Zeile 1 (A1 bis BO1): Enthält die Monatsnamen (z. B. "Jan25,Feb25,...,Mär27").
  - Zeile 2 (A2 bis BO2): Enthält die zugehörigen Kontostände als Zahlen (mit Tausendertrennzeichen und Dezimal-Komma im deutschen Format).
- Ein LaMetric-Display oder eine MyData-App, die JSON-Daten von GitHub abrufen kann.

## Funktionsweise

1. **Datenextraktion:**  
   Mit `extract_data.py` wird der CSV-Export des Google Sheets aus dem Tab „dat“ geladen.  
   - Die erste Zeile wird in eine Liste von Monatsnamen zerlegt.  
   - Die zweite Zeile wird bereinigt (Tausenderpunkte entfernt, Komma in Punkt umgewandelt) und in Floats konvertiert.

2. **Darlehensberechnung:**  
   Das Skript `update_loan.py` berechnet anhand definierter Parameter (Startkapital, Monatsrate, Zinssatz etc.) die tägliche Weiterentwicklung der Restschuld bis zum aktuellen Datum.

3. **Vergleich und Countdown:**  
   Mit `compare_balances.py` wird die Restschuld mit den aus dem Google Sheet extrahierten Kontoständen verglichen. Der erste Monat, in dem der extrahierte Kontostand die Restschuld übersteigt, wird ermittelt. Zusätzlich wird für diesen Monat der Zeitraum (in vollen Monaten und verbleibenden Tagen) von heute bis zum 1. Tag des Zielmonats berechnet.

4. **JSON-Ausgabe:**  
   Das Ergebnis wird in einer JSON-Struktur abgelegt, die beispielsweise so aussieht:

{
"frames": [
{
"text": "Mär27\n9 Monate, 15 Tage",
"icon": "i11386"
},
{
"text": "26722€",
"icon": "i66330"
}
]
}


5. **Automatisierung via GitHub Actions:**  
Der Workflow in .github/workflows/update.yml führt täglich und bei Bedarf manuell die Aktualisierung durch. Die erzeugte `lametric.json` kann direkt von der LaMetric MyData-App abgerufen werden.

## Installation & Nutzung

1. **Repository klonen:**
git clone https://github.com/DaCasio/Giro-Kredi-Comparison.git
cd Giro-Kredi-Comparison


2. **Abhängigkeiten installieren:**
pip install -r requirements.txt


3. **Lokale Ausführung zur Überprüfung:**
python update_loan.py
python compare_balances.py
cat lametric.json


4. **GitHub Actions:**  
   Der Workflow wird automatisch täglich um 06:00 UTC (und bei manueller Auslösung) ausgeführt.

## Anpassungen & Hinweise

- **Google Sheet Formatierung:**  
  Achten Sie darauf, dass im Google Sheet die Monatsnamen und Kontostände korrekt hinterlegt sind. Die Monatsnamen sollten im Format (z. B. "Jan25", "Mär27") vorliegen, damit der Parser sie korrekt in ein Datum umwandeln kann.

- **Zahlenformat:**  
  Die Verarbeitung entfernt Tausendertrennzeichen und konvertiert dezimale Kommas in Punkte. Sollten andere Formate verwendet werden, passen Sie den Code in `extract_data.py` entsprechend an.

- **Debugging:**  
  Falls Probleme auftreten, können die Debug-Ausgaben in den Skripten (und in den GitHub Actions Logs) bei der Fehlersuche helfen.

## Lizenz

Dieses Projekt wird unter der MIT-Lizenz bereitgestellt. Details finden Sie in der LICENSE-Datei.
