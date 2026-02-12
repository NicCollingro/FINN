"""
CONSPIRACY FINN - X/Twitter Scraper
====================================

Scraped Verschwörungstheorien von X/Twitter
Weil normale passiv-aggressive Antworten zu langweilig sind 🛸
"""

import requests
import json
import time
import re
from datetime import datetime

print("=" * 70)
print("CONSPIRACY FINN - X/TWITTER SCRAPER")
print("=" * 70)
print()


# WICHTIG: X/Twitter API ist kompliziert und kostenpflichtig geworden
# ===================================================================
print("⚠️  HINWEIS: X/Twitter API ist seit 2023 kostenpflichtig!")
print()
print("ALTERNATIVE METHODEN:")
print("-" * 70)
print("1. Nitter (Twitter ohne Login)")
print("2. Web Scraping (langsam, kann geblockt werden)")
print("3. Manuelle Daten-Sammlung")
print("-" * 70)
print()


# Conspiracy Keywords
# ===================
CONSPIRACY_KEYWORDS = [
    "chemtrails", "flache erde", "flat earth", "illuminati",
    "neue weltordnung", "nwo", "reptiloiden", "reptilians",
    "deep state", "big pharma", "5g", "microchip",
    "fake news", "mainstream media", "msm", "hoax",
    "false flag", "crisis actors", "wake up", "sheeple",
    "do your research", "follow the money", "they dont want you to know",
    "bill gates", "soros", "rothschild", "freemasons"
]


# Nitter Scraping (Twitter ohne API)
# ===================================
NITTER_INSTANCES = [
    "nitter.net",
    "nitter.poast.org",
    "nitter.privacydev.net",
]

def scrape_nitter(query, instance="nitter.net", limit=50):
    """
    Scraped Tweets von Nitter (Twitter-Mirror ohne Login)
    """
    print(f"\n🔍 Suche nach: '{query}' auf {instance}...")
    
    url = f"https://{instance}/search?f=tweets&q={query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    tweets = []
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Simple HTML Parsing (nicht perfekt aber funktioniert)
            text = response.text
            
            # Finde Tweet-Texte (sehr basic parsing)
            tweet_pattern = r'<div class="tweet-content.*?>(.*?)</div>'
            matches = re.findall(tweet_pattern, text, re.DOTALL)
            
            for match in matches[:limit]:
                # Bereinige HTML
                clean = re.sub(r'<.*?>', '', match)
                clean = clean.strip()
                
                if len(clean) > 20 and len(clean) < 280:
                    tweets.append(clean)
            
            print(f"   ✅ {len(tweets)} Tweets gefunden")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            print(f"   💡 Tipp: Nitter-Instanz könnte down sein, versuche eine andere")
    
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    return tweets


# Alternative: Vorgefertigter Conspiracy Datensatz
# =================================================
def create_manual_conspiracy_dataset():
    """
    Erstellt einen manuellen Datensatz mit typischen Conspiracy-Phrasen
    Falls Scraping nicht funktioniert
    """
    conspiracy_data = [
        "Wacht auf Leute!",
        "Die wollen dass ihr das glaubt.",
        "Macht eure eigene Recherche!",
        "Das ist alles orchestriert.",
        "Zufall? Ich glaube nicht!",
        "Die Mainstream Medien verschweigen das.",
        "Folgt der Spur des Geldes.",
        "Das ist nur die Spitze des Eisbergs.",
        "Sie kontrollieren alles.",
        "Die Wahrheit wird unterdrückt.",
        "Das ist kein Zufall.",
        "Oeffnet eure Augen!",
        "Die Elite will nicht dass ihr das wisst.",
        "Das steckt System dahinter.",
        "Alles ist miteinander verbunden.",
        "Schafe werden das nie verstehen.",
        "Die Zeichen sind überall.",
        "Das wurde schon vor Jahren geplant.",
        "Nichts passiert zufällig.",
        "Sie lügen euch an.",
        "Das Volk wird manipuliert.",
        "Cui bono? Wem nützt es?",
        "Die wollen uns alle kontrollieren.",
        "Das ist ein Ablenkungsmanöver.",
        "Dahinter steckt eine Agenda.",
        "Die Eliten wissen Bescheid.",
        "Das wird vertuscht.",
        "Informiert euch selbst!",
        "Glaubt nicht alles was man euch erzählt.",
        "Das passt zu perfekt zusammen.",
        "Sie haben Angst dass die Wahrheit rauskommt.",
        "Das ist koordiniert.",
        "Alles nach Plan.",
        "Die Timeline passt zu gut.",
        "Das ist gewollt so.",
        "Zufall gibt es nicht.",
        "Die verstecken etwas.",
        "Denkt selbst nach!",
        "Das ergibt keinen Sinn... oder doch?",
        "Sehr verdächtig das Ganze.",
        "Das ist doch offensichtlich.",
        "Sie halten uns für dumm.",
        "Das wird noch rauskommen.",
        "Die Beweise sind überall.",
        "Wer profitiert davon?",
        "Das ist nur Propaganda.",
        "Sie wollen uns spalten.",
        "Teile und herrsche.",
        "Das Muster ist eindeutig.",
        "So naiv kann man doch nicht sein.",
        "Macht die Augen auf!",
        "Das ist alles Theater.",
        "Sie lenken uns ab.",
        "Die Wahrheit liegt auf der Hand.",
        "Das wird verschwiegen.",
        "Zufall? Niemals!",
        "Sie haben einen Plan.",
        "Das ist orchestriert von oben.",
        "Die Masse schläft noch.",
        "Bald wird alles rauskommen.",
        "Die Beweise stapeln sich.",
        "Das ist doch klar ersichtlich.",
        "Sie fürchten die Wahrheit.",
        "Das Establishment will das nicht.",
        "Fragt euch mal warum.",
        "Das timing ist perfekt.",
        "Zu viele Zufälle.",
        "Das stinkt doch zum Himmel.",
        "Die Fakten sprechen für sich.",
        "Man muss nur die Punkte verbinden.",
        "Das ist alles inszeniert.",
        "Die Antworten sind da draussen.",
        "Sie unterschätzen uns.",
        "Das kommt nicht von ungefähr.",
        "Fragt die richtigen Fragen!",
        "Das System ist korrupt.",
        "Die Lügen werden aufgedeckt.",
        "Alles kommt ans Licht.",
        "Die Zeit der Wahrheit kommt.",
        "Sie können es nicht mehr verstecken.",
        "Das Kartenhaus fällt bald.",
        "Die Menschen wachen auf.",
        "Es ist alles miteinander verknüpft.",
        "Das ist größer als ihr denkt.",
        "Schaut hinter die Fassade.",
        "Nichts ist wie es scheint.",
        "Die Realität ist anders.",
        "Sie lügen uns seit Jahren an.",
        "Das ist der Beweis!",
        "Endlich sehen es mehr Leute.",
        "Das haben sie gut versteckt.",
        "Aber die Wahrheit siegt.",
        "Sie verlieren die Kontrolle.",
        "Das System bröckelt.",
        "Jetzt wird aufgeräumt.",
        "Die Masken fallen.",
        "Glaubt nicht alles blind.",
        "Hinterfragt alles!",
        "Das ist nur die offizielle Version.",
        "Die wahre Geschichte ist anders.",
    ]
    
    return conspiracy_data


# HAUPT-FUNKTION
# ==============
print("=" * 70)
print("🚀 STARTE DATEN-SAMMLUNG")
print("=" * 70)
print()

all_data = []

# Methode 1: Versuche Nitter
print("Methode 1: Nitter Scraping")
print("-" * 70)

for keyword in CONSPIRACY_KEYWORDS[:5]:  # Erste 5 Keywords
    for instance in NITTER_INSTANCES[:2]:  # Erste 2 Instanzen
        tweets = scrape_nitter(keyword, instance=instance, limit=20)
        all_data.extend(tweets)
        time.sleep(2)  # Rate limiting
        
        if len(all_data) > 100:
            break
    
    if len(all_data) > 100:
        break

print()
print(f"📊 Von Nitter: {len(all_data)} Tweets")
print()

# Methode 2: Manueller Datensatz (Backup)
print("Methode 2: Manueller Conspiracy Datensatz")
print("-" * 70)

manual_data = create_manual_conspiracy_dataset()
all_data.extend(manual_data)

print(f"✅ {len(manual_data)} manuelle Einträge hinzugefügt")
print()

# Duplikate entfernen
all_data = list(set(all_data))

print("=" * 70)
print(f"✅ TOTAL: {len(all_data)} Einträge gesammelt")
print("=" * 70)
print()


# Speichern
# =========
if len(all_data) > 0:
    print("💾 Speichere Daten...")
    
    with open('conspiracy_training_data.txt', 'w', encoding='utf-8') as f:
        for entry in all_data:
            f.write(entry + '\n')
    
    print("✅ Gespeichert als: conspiracy_training_data.txt")
    
    # JSON mit Metadaten
    data_json = {
        'created_at': datetime.now().isoformat(),
        'type': 'conspiracy_theories',
        'total_entries': len(all_data),
        'entries': all_data
    }
    
    with open('conspiracy_training_data.json', 'w', encoding='utf-8') as f:
        json.dump(data_json, f, indent=2, ensure_ascii=False)
    
    print("✅ Gespeichert als: conspiracy_training_data.json")
    print()
    
    # Statistiken
    print("=" * 70)
    print("📊 STATISTIKEN")
    print("=" * 70)
    print(f"Total Einträge: {len(all_data)}")
    print(f"Total Zeichen: {sum(len(e) for e in all_data)}")
    print(f"Durchschnitt: {sum(len(e) for e in all_data) / len(all_data):.1f} Zeichen")
    print()
    
    # Beispiele
    print("📝 BEISPIELE:")
    print("-" * 70)
    for i, entry in enumerate(all_data[:15], 1):
        print(f"{i}. {entry}")
    print("-" * 70)

print()
print("=" * 70)
print("🎉 FERTIG!")
print("=" * 70)
print()
print("Nächster Schritt:")
print("  python finn_v2_train.py")
print()
print("💡 Tipp: Passe finn_v2_train.py an um")
print("         'conspiracy_training_data.txt' zu laden!")
