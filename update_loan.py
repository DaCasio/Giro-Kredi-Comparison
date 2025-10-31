from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN, getcontext
import json

getcontext().prec = 8

darlehen = {
    'start_date': date(2023, 8, 15),
    'end_date': date(2030, 3, 15),
    'start_kapital': Decimal('32000.00'),
    'monatsrate': Decimal('503.16'),
    'zins_satz': Decimal('6.74') / 100,
    'zinsmethode': '30/360'
}

def berechne_tägliche_zinsen(kapital: Decimal) -> Decimal:
    return (kapital * darlehen['zins_satz']) / 360

def darlehens_entwicklung(target_date: date) -> Decimal:
    current_date = darlehen['start_date']
    kapital = darlehen['start_kapital']
    
    while current_date <= target_date:
        if current_date.day == 15 and current_date > darlehen['start_date']:
            kapital -= darlehen['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        else:
            kapital += berechne_tägliche_zinsen(kapital)
        
        current_date += timedelta(days=1)
    
    return kapital.quantize(Decimal('1'), rounding=ROUND_DOWN)

def generiere_json():
    aktueller_stand = darlehens_entwicklung(date.today())
    return {
        "frames": [
            {
                "text": f"{int(aktueller_stand)}€",
                "icon": "616",
                "goalData": {
                    "start": 32000,
                    "current": int(aktueller_stand),
                    "end": 0,
                    "unit": "€"
                }
            }
        ]
    }

if __name__ == "__main__":
    with open("darlehen.json", "w") as f:
        json.dump(generiere_json(), f, indent=2, ensure_ascii=False)
    
    # Validierung mit bekanntem Wert vom 15.09.2023
    if date.today() == date(2023, 9, 15):
        aktueller_wert = darlehens_entwicklung(date(2023, 9, 15))
        assert 31502 <= aktueller_wert <= 31503, f"Abweichung: {aktueller_wert}€ statt 31502€"
