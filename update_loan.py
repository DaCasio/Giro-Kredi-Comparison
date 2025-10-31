from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP, getcontext
import json

getcontext().prec = 10

# Historische echte Kontostände aus der Umsatzliste
HISTORISCHE_DATEN = {
    date(2023, 7, 15): Decimal('32000.00'),
    date(2023, 8, 15): Decimal('31682.08'),
    date(2023, 9, 15): Decimal('31362.37'),
    date(2023, 10, 15): Decimal('31040.86'),
    date(2023, 11, 15): Decimal('30717.55'),
    date(2023, 12, 15): Decimal('30392.42'),
    date(2024, 1, 15): Decimal('30065.46'),
    date(2024, 2, 15): Decimal('29736.67'),
    date(2024, 3, 15): Decimal('29406.03'),
    date(2024, 4, 15): Decimal('29073.53'),
    date(2024, 5, 15): Decimal('28739.16'),
    date(2024, 6, 15): Decimal('28402.92'),
    date(2024, 7, 15): Decimal('28064.79'),
    date(2024, 8, 15): Decimal('27724.76'),
    date(2024, 9, 15): Decimal('27382.82'),
    date(2024, 10, 15): Decimal('27038.96'),
    date(2024, 11, 15): Decimal('26693.16'),
    date(2024, 12, 15): Decimal('26345.42'),
    date(2025, 1, 15): Decimal('25995.73'),
    date(2025, 2, 15): Decimal('25644.07'),
    date(2025, 3, 15): Decimal('25290.44'),
    date(2025, 4, 15): Decimal('24934.82'),
    date(2025, 5, 15): Decimal('24577.20'),
    date(2025, 6, 15): Decimal('24217.57'),
    date(2025, 7, 15): Decimal('23855.92'),
    date(2025, 8, 15): Decimal('23492.24'),
    date(2025, 9, 15): Decimal('23126.52'),
    date(2025, 10, 15): Decimal('22758.74'),
}

# Tilgungsplan ab November 2025
TILGUNGSPLAN = {
    date(2025, 11, 15): Decimal('22388.90'),
    date(2025, 12, 15): Decimal('22016.98'),
    date(2026, 1, 15): Decimal('21642.97'),
    date(2026, 2, 15): Decimal('21266.86'),
    date(2026, 3, 15): Decimal('20888.63'),
    date(2026, 4, 15): Decimal('20508.28'),
    date(2026, 5, 15): Decimal('20125.79'),
    date(2026, 6, 15): Decimal('19741.15'),
    date(2026, 7, 15): Decimal('19354.35'),
    date(2026, 8, 15): Decimal('18965.38'),
    date(2026, 9, 15): Decimal('18574.22'),
    date(2026, 10, 15): Decimal('18180.87'),
    date(2026, 11, 15): Decimal('17785.31'),
    date(2026, 12, 15): Decimal('17387.52'),
    date(2027, 1, 15): Decimal('16987.50'),
    date(2027, 2, 15): Decimal('16585.23'),
    date(2027, 3, 15): Decimal('16180.70'),
    date(2027, 4, 15): Decimal('15773.90'),
    date(2027, 5, 15): Decimal('15364.81'),
    date(2027, 6, 15): Decimal('14953.42'),
    date(2027, 7, 15): Decimal('14539.72'),
    date(2027, 8, 15): Decimal('14123.70'),
    date(2027, 9, 15): Decimal('13705.34'),
    date(2027, 10, 15): Decimal('13284.63'),
    date(2027, 11, 15): Decimal('12861.56'),
    date(2027, 12, 15): Decimal('12436.11'),
    date(2028, 1, 15): Decimal('12008.27'),
    date(2028, 2, 15): Decimal('11578.03'),
    date(2028, 3, 15): Decimal('11145.37'),
    date(2028, 4, 15): Decimal('10710.28'),
    date(2028, 5, 15): Decimal('10272.74'),
    date(2028, 6, 15): Decimal('9832.75'),
    date(2028, 7, 15): Decimal('9390.28'),
    date(2028, 8, 15): Decimal('8945.33'),
    date(2028, 9, 15): Decimal('8497.88'),
    date(2028, 10, 15): Decimal('8047.91'),
    date(2028, 11, 15): Decimal('7595.42'),
    date(2028, 12, 15): Decimal('7140.38'),
    date(2029, 1, 15): Decimal('6682.79'),
    date(2029, 2, 15): Decimal('6222.63'),
    date(2029, 3, 15): Decimal('5759.88'),
    date(2029, 4, 15): Decimal('5294.53'),
    date(2029, 5, 15): Decimal('4826.57'),
    date(2029, 6, 15): Decimal('4355.98'),
    date(2029, 7, 15): Decimal('3882.74'),
    date(2029, 8, 15): Decimal('3406.84'),
    date(2029, 9, 15): Decimal('2928.27'),
    date(2029, 10, 15): Decimal('2447.01'),
    date(2029, 11, 15): Decimal('1963.05'),
    date(2029, 12, 15): Decimal('1476.37'),
    date(2030, 1, 15): Decimal('986.95'),
    date(2030, 2, 15): Decimal('494.79'),
    date(2030, 3, 15): Decimal('0.00'),
}

# Kombiniere historische Daten mit Tilgungsplan
ALLE_STICHTAGE = {**HISTORISCHE_DATEN, **TILGUNGSPLAN}

def darlehens_entwicklung(target_date: date) -> Decimal:
    """
    Berechnet den interpolierten Kontostand für ein beliebiges Datum.
    Verwendet echte historische Daten und Tilgungsplan.
    """
    # Wenn target_date ein Stichtag ist, direkt zurückgeben
    if target_date in ALLE_STICHTAGE:
        return ALLE_STICHTAGE[target_date]
    
    # Finde den vorherigen und nächsten Stichtag
    stichtag_liste = sorted(ALLE_STICHTAGE.keys())
    
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
        return Decimal('32000.00')
    if naechster_stichtag is None:
        return max(Decimal('0'), ALLE_STICHTAGE[vorheriger_stichtag])
    
    # Lineare Interpolation zwischen den beiden Stichtagen
    start_wert = ALLE_STICHTAGE[vorheriger_stichtag]
    end_wert = ALLE_STICHTAGE[naechster_stichtag]
    
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
    
    print("=== VALIDIERUNG MIT ECHTEN DATEN ===\n")
    
    # Test mit echten historischen Daten
    print("Historische Daten (aus Umsatzliste):")
    test_datum_okt_2025 = date(2025, 10, 15)
    wert_okt_2025 = darlehens_entwicklung(test_datum_okt_2025)
    print(f"15.10.2025: {wert_okt_2025:.2f}€ (Soll: 22.758,74€)")
    
    test_datum_sep_2023 = date(2023, 9, 15)
    wert_sep_2023 = darlehens_entwicklung(test_datum_sep_2023)
    print(f"15.09.2023: {wert_sep_2023:.2f}€ (Soll: 31.362,37€)")
    
    # Test mit Tilgungsplan
    print("\nZukünftige Daten (aus Tilgungsplan):")
    test_datum_nov = date(2025, 11, 15)
    wert_nov = darlehens_entwicklung(test_datum_nov)
    print(f"15.11.2025: {wert_nov:.2f}€ (Soll: 22.388,90€)")
    
    test_datum_dez = date(2025, 12, 15)
    wert_dez = darlehens_entwicklung(test_datum_dez)
    print(f"15.12.2025: {wert_dez:.2f}€ (Soll: 22.016,98€)")
    
    test_datum_ende = date(2030, 3, 15)
    wert_ende = darlehens_entwicklung(test_datum_ende)
    print(f"15.03.2030: {wert_ende:.2f}€ (Soll: 0,00€)")
    
    # Test interpolierter Wert heute
    print(f"\n=== AKTUELLER INTERPOLIERTER STAND ===")
    heute = date.today()
    wert_heute = darlehens_entwicklung(heute)
    print(f"Heute ({heute.strftime('%d.%m.%Y')}): {wert_heute:.2f}€")
    
    # Berechne tägliche Reduktion bis 15.11.
    naechster_stichtag = date(2025, 11, 15)
    tage_bis_stichtag = (naechster_stichtag - heute).days
    differenz = wert_heute - Decimal('22388.90')
    if tage_bis_stichtag > 0:
        taeglich = differenz / tage_bis_stichtag
        print(f"Tägliche Reduktion bis 15.11.: {taeglich:.2f}€")
    
    print("\n✓ Alle Daten erfolgreich geladen!")
