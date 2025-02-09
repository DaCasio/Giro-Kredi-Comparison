# compare_balances.py
import json

# ... existierender Code ...

with open('lametric.json', 'w') as f:
    json.dump(output, f)

# Fallback, falls kein Monat gefunden
if not os.path.exists('lametric.json'):
    with open('lametric.json', 'w') as f:
        json.dump({"frames": [{"text": "Keine Daten", "icon": "i17911"}]}, f)
