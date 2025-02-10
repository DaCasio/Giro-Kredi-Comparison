import json
from datetime import date
from extract_data import extract_data
from update_loan import darlehens_entwicklung

def get_target_month(loan_balance):
    months, balances = extract_data()
    
    # Überprüfen, ob gültige Daten vorliegen
    if len(months) == 0 or len(balances) == 0:
        return "Datenfehler", 0
    
    print(f"DEBUG: Loan balance to compare: {loan_balance}")
    print(f"DEBUG: Balances from sheet: {balances}")
    
    # Durchlaufen der Kontostände und Vergleich mit der Restschuld
    for idx, balance in enumerate(balances):
        print(f"DEBUG: Comparing balance {balance} with loan balance {loan_balance}")
        if balance > loan_balance:
            return months[idx], balance
    
    return "Nicht vorhersagbar", 0

if __name__ == "__main__":
    try:
        current_loan = darlehens_entwicklung(date.today())
    except Exception as e:
        print(f"Fehler beim Berechnen der Restschuld: {str(e)}")
        current_loan = 0  # Fallback-Wert
    
    result, summe = get_target_month(current_loan)
    
    # JSON-Ausgabe für den Monat
    output_monat = {
        "frames": [
            {
                "text": f"{result}",
                "icon": "i616"  # Euro-Symbol
            }
        ]
    }
    
    # JSON-Ausgabe für die Summe
    output_summe = {
        "frames": [
            {
                "text": f"{int(summe)}€",
                "icon": "i616"  # Euro-Symbol
            }
        ]
    }
    
    with open('lametric-monat.json', 'w') as f:
        json.dump(output_monat, f)
    
    with open('lametric-summe.json', 'w') as f:
        json.dump(output_summe, f)
