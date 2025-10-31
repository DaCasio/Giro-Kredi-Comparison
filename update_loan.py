from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP, getcontext
import json

getcontext().prec = 10

darlehen = {
    'start_date': date(2023, 8, 15),
    'end_date': date(2030, 3, 15),
    'start_kapital': Decimal('32000.00'),
    'monatsrate': Decimal('497.71'),
    'zins_satz': Decimal('6.74') / 100
}

def berechne_monatliche_zinsen(kapital: Decimal) -> Decimal:
    """Berechnet die monatlichen Zinsen"""
    zinsen = (kapital * darlehen['zins_satz']) / 12
    return zinsen.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def berechne_stichtagswerte() -> dict:
    """
    Berechnet die echten Kontostände am 15. jeden Monats
    bis zum Laufzeitende oder bis Restschuld = 0
    """
    stichtage = {}
    current_date = darlehen['start_date']
    kapital = darlehen['start_kapital']
    
    # Startdatum speichern
    stichtage[current_date] = kapital
    
    while current_date < darlehen['end_date']:
        # Zum nächsten 15. springen
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 15)
        else:
            current_date = date(current_date.year, current_date.month + 1, 15)
        
        # Monatszinsen aufschlagen
        monatszinsen = berechne_monatliche_zinsen(kapital)
        kapital += monatszinsen
        
        # Rate abziehen
        kapital -= darlehen['monatsrate']
        kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Stichtag speichern
        stichtage[current_date] = kapital
        
        # Abbruch wenn vollständig getilgt
        if kapital <= 0:
            break
    
    return stichtage

def darlehens_entwicklung(target_date: date) -> Decimal:
    """
    Berechnet den interpolierten Kontostand für ein beliebiges Datum.
    Zwischen zwei Stichtagen (15. des Monats) wird LINEAR interpoliert.
    """
    stichtage = berechne_stichtagswerte()
    
    # Wenn target_date ein Stichtag ist, direkt zurückgeben
    if target_date in stichtage:
        return stichtage[target_date]
    
    # Finde den vorherigen und nächsten Stichtag
    stichtag_liste = sorted(stichtage.keys())
    
    vorheriger_stichtag = None
    naechster_stichtag = None
    
    for stichtag in stichtag_liste:
        if stichtag <= target_date:
            vorheriger_stichtag = stichtag
        if stichtag > target_date and naechster_stichtag is None:
            naechster_stichtag = stichtag
            break
    
    # Falls target_date vor dem Start oder nach dem Ende liegt
    if vorheriger_stichtag is None:
        return darlehen['start_kapital']
    if naechster_stichtag is None:
        # Nach dem letzten Stichtag: Restschuld ist 0 oder letzter Wert
        letzter_wert = stichtage[vorheriger_stichtag]
        return max(Decimal('0'), letzter_wert)
    
    # Lineare Interpolation zwischen den beiden Stichtagen
    start_wert = stichtage[vorheriger_stichtag]
    end_wert = stichtage[naechster_stichtag]
    
    # Tage zwischen den Stichtagen
    tage_gesamt = (naechster_stichtag - vorheriger_stichtag).days
    tage_vergangen = (target_date - vorheriger_stichtag).days
    
    # Tägliche Reduktion berechnen
    differenz = start_wert - end_wert
    taegliche_reduktion = differenz / tage_gesamt
    
    # Interpolierter Wert
    interpolierter_wert = start_wert - (taegliche_reduktion * tage_vergangen)
    
    return interpolierter_wert.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

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
    
    # Validierung mit echten Bankdaten
    test_datum_okt = date(2025, 10, 15)
    wert_okt = darlehens_entwicklung(test_datum_okt)
    print(f"15.10.2025: {wert_okt:.2f}€ (Soll: 22.758,74€)")
    
    test_datum_nov = date(2025, 11, 15)
    wert_nov = darlehens_entwicklung(test_datum_nov)
    print(f"15.11.2025: {wert_nov:.2f}€ (Soll: 22.388,90€)")
    
    test_datum_dez = date(2025, 12, 15)
    wert_dez = darlehens_entwicklung(test_datum_dez)
    print(f"15.12.2025: {wert_dez:.2f}€ (Soll: 22.016,98€)")
    
    # Assertions
    assert abs(wert_okt - Decimal('22758.74')) < Decimal('1.00'), f"Fehler Oktober: {wert_okt}€"
    assert abs(wert_nov - Decimal('22388.90')) < Decimal('1.00'), f"Fehler November: {wert_nov}€"
    assert abs(wert_dez - Decimal('22016.98')) < Decimal('1.00'), f"Fehler Dezember: {wert_dez}€"
    
    print("✓ Alle Validierungen erfolgreich!")
