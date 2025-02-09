# Giro-Kredi-Comparison

Dieses Projekt vergleicht den Kontostand aus einem öffentlichen Google Sheets-Dokument mit dem aktuellen Darlehensstand und ermittelt den Monat, in dem der Kontostand den Darlehensstand übersteigt. Die Ergebnisse werden in einer JSON-Datei gespeichert, die von der Lametric My Data App gelesen werden kann.

## Voraussetzungen

- Python 3.x
- `pandas` Bibliothek

## Installation

1. **Klonen Sie das Repository:**

git clone https://github.com/IhrGitHubName/Giro-Kredi-Comparison.git


2. **Installieren Sie die benötigten Pakete:**

pip install pandas


## Nutzung

1. **Daten extrahieren:**

python extract_data.py


2. **Vergleich durchführen:**

python compare_balances.py


- Der aktuelle Darlehensstand muss in der Datei `compare_balances.py` angepasst werden.

3. **Ergebnisse anzeigen:**
- Die Ergebnisse werden in `lametric_output.json` gespeichert, die von der Lametric My Data App gelesen werden kann.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die `LICENSE`-Datei für Details.

LICENSE

MIT License

Copyright (c) [Jahr] [Ihr Name]

Erlaubnis hiermit, kostenlos, jeder Person, die eine Kopie dieser Software und der zugehörigen Dokumentationsdateien (die "Software") erhält, ohne Einschränkung mit der Software zu handeln, einschließlich, aber nicht beschränkt auf, die Rechte, die Software zu verwenden, zu kopieren, zu modifizieren, zu fusionieren, zu veröffentlichen, zu verteilen, Unterlizenzen zu gewähren und/oder zu verkaufen, und Personen, denen die Software zur Verfügung gestellt wird, dies zu erlauben, unter den folgenden Bedingungen:

Die obige Urheberrechtsbenachrichtigung und diese Erlaubnisbenachrichtigung müssen in allen Kopien oder wesentlichen Teilen der Software enthalten sein.

DIE SOFTWARE WIRD "WIE SIE IST" BEREITGESTELLT, OHNE JEGLICHE GARANTIE, AUSDRÜCKLICH ODER STILLSCHWEIGEND, EINSCHLIESSLICH, ABER NICHT BESCHRÄNKT AUF, DIE GARANTIEN DER MARKTGÄNGIGKEIT, DER EIGNUNG FÜR EINEN BESTIMMTEN ZWECK UND DER NICHTVERLETZUNG. IN KEINEM FALL SIND DIE AUTOREN ODER URHEBERRECHTSINHABER FÜR JEGLICHE ANSPRÜCHE, SCHÄDEN ODER ANDERE VERPFLICHTUNGEN VERANTWORTLICH, OB AUS VERTRAG, DELIKT ODER ANDERWEITIG, ENTSTANDEN AUS, AUS ODER IN VERBINDUNG MIT DER SOFTWARE ODER DER NUTZUNG ODER ANDEREN HANDLUNGEN MIT DER SOFTWARE.

