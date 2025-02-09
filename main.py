import pandas as pd

# URL des öffentlichen Google Sheets-Dokuments
url = "https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv&gid=0"

# Daten in ein DataFrame laden
data = pd.read_csv(url)

# Monatsnamen und Kontostände extrahieren
monthly_names = data.iloc[0, :].values  # A1 bis BY1
monthly_balances = data.iloc[1, :].values  # A2 bis BY2

# Ausgabe der extrahierten Daten
print("Monatsnamen:", monthly_names)
print("Kontostände:", monthly_balances)
