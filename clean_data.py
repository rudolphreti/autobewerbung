import json
import re

def clean_company_strings(data):
    patterns_to_remove = [
        r'\(mwd\)',
        r'\(w/m/d\)',
        r'm/w/d',
        r'\(m/w/d\)',
        r'/in',
        r':in',
        r'\(f/m/d\)',
        r'\(w/m/\*\)',
        r'\(m/f/x\)',
        r'\(M/W\)',
        r'\(m/w/d\)'
    ]
    
    pattern = '|'.join(patterns_to_remove)
    
    for item in data:
        if 'company' in item:
            item['company'] = re.sub(pattern, '', item['company']).strip()
        if 'position' in item:
            item['position'] = re.sub(pattern, '', item['position']).strip()
    
    return data

# Daten aus der JSON-Datei lesen
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Funktion aufrufen
cleaned_data = clean_company_strings(data)

# Bereinigte Daten zurück in die ursprüngliche JSON-Datei schreiben
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

print("Bereinigung abgeschlossen. Die Ergebnisse wurden in 'data.json' aktualisiert.")

# Optional: Ausgabe der bereinigten Unternehmensnamen und Positionen
for item in cleaned_data:
    print(f"Company: {item['company']}")
    print(f"Position: {item['position']}")
    print("---")