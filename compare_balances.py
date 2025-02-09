import json
from datetime import date
from extract_data import extract_data
from update_loan import darlehens_entwicklung

def get_target_month(loan_balance):
    months, balances = extract_data()
    
    # Statt "if not months or not balances:" nun:
    if len(months) == 0 or len(balances) == 0:
        return "Datenfehler"
    
    print(f"DEBUG: Loan balance to compare: {loan_balance}")
    print(f"DEBUG: Balances from sheet: {balances}")
    
    # Durchlaufen der Kontostände und Vergleich mit der Restschuld
    for idx, balance in enumerate(balances):
        print(f"DEBUG: Comparing balance {balance} with loan balance {loan_balance}")
        if balance > loan_balance:
            return months[idx]
    
    return "Nicht vorhersagbar"

if __name__ == "__main__":
    try:
        current_loan = darlehens_entwicklung(date.today())
    except Exception as e:
        print(f"Fehler beim Berechnen der Restschuld: {str(e)}")
        current_loan = 0
    result = get_target_month(current_loan)
    
    output = {
        "frames": [
            {
                "text": f"{result}",
                "icon": "i17911"
            }
        ]
    }
    
    with open('lametric.json', 'w') as f:
        json.dump(output, f)
