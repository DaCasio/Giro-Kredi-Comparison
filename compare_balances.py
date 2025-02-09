# compare_balances.py (AKTUALISIERT)
from extract_data import extract_data

def get_target_month(loan_balance):
    months, balances = extract_data()
    
    if not len(months) or not len(balances):
        return "Datenfehler"
    
    for idx, balance in enumerate(balates):
        if balance > loan_balance:
            return months[idx]
    return "Nicht vorhersagbar"
