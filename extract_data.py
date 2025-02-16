import pandas as pd

def extract_data():
    url = "https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv&gid=0"
    try:
        # CSV-Daten laden
        data = pd.read_csv(url, header=None)  # Keine Kopfzeile verwenden
        
        # Debug-Ausgabe des gesamten DataFrames
        print(f"DEBUG: Raw data from Google Sheet:\n{data}")
        
        # Überprüfen, ob mindestens zwei Zeilen vorhanden sind
        if data.shape[0] < 2:
            raise ValueError("Google Sheet hat weniger als 2 Zeilen")
        
        # Extrahieren der Monatsnamen und Kontostände aus Zeile 1 und 2
        months = data.iloc[0, :].values  # Zeile 1: Monatsnamen
        balances = [
            float(value.replace(".", "").replace(",", ".").strip())  # Tausendertrennzeichen entfernen, Dezimalpunkt setzen
            for value in data.iloc[1, :].values  # Zeile 2: Kontostände
        ]
        
        print(f"DEBUG: Extracted months: {months}")
        print(f"DEBUG: Extracted balances: {balances}")
        
        return months, balances
    except Exception as e:
        print(f"Fehler beim Laden der Daten: {str(e)}")
        return [], []

if __name__ == "__main__":
    months, balances = extract_data()
    print(f"Monate: {months}\nKontostände: {balances}")
