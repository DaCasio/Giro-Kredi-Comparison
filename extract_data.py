import pandas as pd

def extract_data():
    url = "https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv"
    try:
        # CSV-Daten laden
        data = pd.read_csv(url)
        
        # Überprüfen, ob mindestens zwei Zeilen vorhanden sind
        if data.shape[0] < 2:
            raise ValueError("Google Sheet hat weniger als 2 Zeilen")
        
        # Extrahieren der Monatsnamen und Kontostände
        months = data.iloc[0].values
        balances = data.iloc[1].values
        
        # Sicherstellen, dass keine NaN-Werte vorhanden sind
        if any(pd.isna(months)) or any(pd.isna(balances)):
            raise ValueError("Google Sheet enthält ungültige oder fehlende Werte")
        
        return months, balances
    except Exception as e:
        print(f"Fehler beim Laden der Daten: {str(e)}")
        return [], []

if __name__ == "__main__":
    months, balances = extract_data()
    print(f"Monate: {months}\nKontostände: {balances}")
