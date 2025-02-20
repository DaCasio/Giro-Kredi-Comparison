import json
from datetime import date
from calendar import monthrange
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

def parse_month(month_str):
    """
    Wandelt einen Monatsstring, z. B. "Jan25" oder "Mär27", in ein date-Objekt um.
    Es wird davon ausgegangen, dass der Monatsname immer dreistellig und die Jahreszahl zweistellig ist.
    """
    month_part = month_str[:3]
    year_part = month_str[3:]
    if len(year_part) != 2:
        raise ValueError("Ungültiger Jahres-Teil im Monat: " + month_str)
    year_full = int("20" + year_part)
    month_map = {
        'Jan': 1,
        'Feb': 2,
        'Mär': 3,
        'Apr': 4,
        'Mai': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Okt': 10,
        'Nov': 11,
        'Dez': 12,
    }
    if month_part not in month_map:
        raise ValueError("Unbekannter Monatsname: " + month_part)
    return date(year_full, month_map[month_part], 1)

def add_months(orig_date, months):
    """
    Addiert eine bestimmte Anzahl von Monaten zu orig_date.
    Falls der Tag im Zielmonat nicht existiert, wird der letzte gültige Tag gewählt.
    """
    new_month = orig_date.month - 1 + months
    new_year = orig_date.year + new_month // 12
    new_month = new_month % 12 + 1
    new_day = orig_date.day
    max_day = monthrange(new_year, new_month)[1]
    if new_day > max_day:
        new_day = max_day
    return date(new_year, new_month, new_day)

def calculate_months_and_days_exact(start_date, end_date):
    """
    Berechnet die exakten vollen Monate und verbleibenden Tage zwischen zwei Daten.
    Beispiel: Vom 16.02.2025 bis 01.12.2025 ergibt 9 Monate und 15 Tage.
    """
    total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    if start_date.day > end_date.day:
        total_months -= 1
    anchor_date = add_months(start_date, total_months)
    days_remainder = (end_date - anchor_date).days
    return total_months, days_remainder

if __name__ == "__main__":
    try:
        current_loan = darlehens_entwicklung(date.today())
    except Exception as e:
        print(f"Fehler beim Berechnen der Restschuld: {str(e)}")
        current_loan = 0  # Fallback-Wert
    
    result, summe = get_target_month(current_loan)
    
    if result not in ["Datenfehler", "Nicht vorhersagbar"]:
        try:
            target_date = parse_month(result)
            current_date = date.today()
            if target_date <= current_date:
                months_count, days_count = 0, 0
            else:
                months_count, days_count = calculate_months_and_days_exact(current_date, target_date)
                # Einen zusätzlichen Tag hinzufügen, damit z. B. aus 13 Tagen 14 werden
                days_count += 1
            countdown_text = f"M{months_count} T{days_count}"
        except Exception as e:
            print("Fehler beim Berechnen der Zeitdifferenz:", e)
            countdown_text = ""
    else:
        countdown_text = ""
    
    output = {
        "frames": [
            {
                "text": result,
                "icon": "11386"
            },
            {
                "text": countdown_text,
                "icon": "11386"
            },
            {
                "text": f"{int(summe)}€",
                "icon": "66330"
            }
        ]
    }
    
    with open('lametric.json', 'w') as f:
        json.dump(output, f)
