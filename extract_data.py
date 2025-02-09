import pandas as pd
import os

def extract_data():
    url = "https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv"
    try:
        data = pd.read_csv(url)
        if data.shape[0] < 2:
            raise ValueError("Google Sheet hat weniger als 2 Zeilen")
        return data.iloc[0].values, data.iloc[1].values
    except Exception as e:
        print(f"Fehler beim Laden der Daten: {str(e)}")
        return [], []

if __name__ == "__main__":
    months, balances = extract_data()
    print(f"Monate: {months}\nKontostände: {balances}")
