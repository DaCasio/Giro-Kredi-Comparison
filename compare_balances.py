import json
from datetime import date
from extract_data import extract_data
from update_loan import darlehens_entwicklung

def get_target_month(loan_balance):
    months, balances = extract_data()
    
    # Überprüfen, ob gültige Daten vorliegen
    if not months or not balances:
        return "Datenfehler"
    
    # Durchlaufen der Kontostände und Vergleich mit der Restschuld
    for idx, balance in enumerate(balances):
        if balance > loan_balance:
            return months[idx]
    
    return "Nicht vorhersagbar"

if __name__ == "__main__":
    try:
        # Berechnung der aktuellen Restschuld
        current_loan = darlehens_entwicklung(date.today())
    except Exception as e:
        print(f"Fehler beim Berechnen der Restschuld: {str(e)}")
        current_loan = 0  # Fallback-Wert
    
    result = get_target_month(current_loan)
    
    # JSON-Ausgabe für LaMetric erstellen
    output = {
        "frames": [
            {
                "text": f"Kontoüberhang: {result}",
                "icon": "i17911"  # Kalender-Icon
            }
        ]
    }
    
    with open('lametric.json', 'w') as f:
        json.dump(output, f)
