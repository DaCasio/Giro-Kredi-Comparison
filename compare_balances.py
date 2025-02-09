import json
from extract_data import extract_data

def get_target_month(loan_balance):
    months, balances = extract_data()
    for idx, balance in enumerate(balances):
        if balance > loan_balance:
            return months[idx]
    return "Nicht vorhersagbar"

if __name__ == "__main__":
    current_loan = 10000  # Wird durch GitHub Secret ersetzt
    result = get_target_month(current_loan)
    output = {"frames": [{"text": f"Kontoüberhang: {result}", "icon": "i17911"}]}
    with open('lametric.json', 'w') as f:
        json.dump(output, f)
