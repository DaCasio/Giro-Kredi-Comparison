import json
from extract_data import extract_data

def compare_balances(current_loan_balance):
    monthly_names, monthly_balances = extract_data()
    
    for i, balance in enumerate(monthly_balances):
        if balance > current_loan_balance:
            return monthly_names[i]
    
    return "Kein Monat gefunden, in dem der Kontostand den Darlehensstand übersteigt."

if __name__ == "__main__":
    # Beispielwert für den aktuellen Darlehensstand
    current_loan_balance = 10000
    
    result = compare_balances(current_loan_balance)
    
    # JSON-Struktur für Lametric
    output = {
        "frames": [
            {
                "text": f"Der Kontostand übersteigt den Darlehensstand im Monat: {result}",
                "icon": "i12345"  # Hier ein passendes Icon einfügen
            }
        ]
    }

    # JSON-Datei erstellen
    with open('lametric_output.json', 'w') as f:
        json.dump(output, f)
