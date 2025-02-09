import pandas as pd

def extract_data():
    url = "https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv"
    try:
        # CSV-Daten laden
        data = pd.read_csv(url, header=None)  # Keine Kopfzeile verwenden
        
        # Überprüfen, ob mindestens zwei Zeilen vorhanden sind
        if data.shape[0] < 2:
            raise ValueError("Google Sheet hat weniger als 2 Zeilen")
        
        # Extrahieren der Monatsnamen und Kontostände aus Spalte A
        months = data.iloc[0, 0].split(",")  # A1: Monatsnamen durch Kommas getrennt
        balances = [float(value) for value in data.iloc[1, 0].split(",")]  # A2: Kontostände durch Kommas getrennt
        
        return months, balances
    except Exception as e:
        print(f"Fehler beim Laden der Daten: {str(e)}")
        return [], []

if __name__ == "__main__":
    months, balances = extract_data()
    print(f"Monate: {months}\nKontostände: {balances}")
