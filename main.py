import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

# Google Sheets API einrichten
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Google Sheets öffnen
giro_sheet = client.open_by_key('YOUR_GIRO_SHEET_ID').sheet1
kredi_sheet = client.open_by_key('YOUR_KREDI_SHEET_ID').sheet1

# Daten abrufen
giro_data = giro_sheet.get_all_values()
kredi_data = kredi_sheet.get_all_values()

# Vergleichslogik
def compare_data(giro_data, kredi_data):
    for giro_row, kredi_row in zip(giro_data, kredi_data):
        giro_balance = float(giro_row[1])  # Annahme: Kontostand in der zweiten Spalte
        kredi_balance = float(kredi_row[1])  # Annahme: Darlehensstand in der zweiten Spalte
        if giro_balance > kredi_balance:
            return giro_row[0]  # Annahme: Monat in der ersten Spalte
    return None

result = compare_data(giro_data, kredi_data)

if result:
    print(f"Der Kontostand wird im Monat {result} den Darlehensstand übersteigen.")
else:
    print("Der Kontostand wird den Darlehensstand nicht übersteigen.")

# Daten für Lametric vorbereiten
lametric_data = {
    "frames": [
        {
            "text": f"Übersteigung im Monat: {result}",
            "icon": "i616"
        }
    ]
}

with open('lametric_data.json', 'w') as f:
    json.dump(lametric_data, f, indent=2, ensure_ascii=False)
