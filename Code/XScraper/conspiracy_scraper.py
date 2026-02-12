"""
CONSPIRACY FINN - Alternative Scraper
======================================

Scraped von öffentlichen Conspiracy-Websites
Funktioniert robuster als Twitter/Nitter
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

print("=" * 70)
print("CONSPIRACY FINN - ALTERNATIVE SCRAPER")
print("=" * 70)
print()
print("Scraped von öffentlichen Quellen ohne API")
print()


def clean_text(text):
    """Bereinigt Text"""
    # Entferne HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    
    # Entferne URLs
    text = re.sub(r'http\S+', '', text)
    
    # Entferne mehrfache Leerzeichen
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def scrape_reddit_conspiracy():
    """
    Scraped r/conspiracy Titles (öffentlich, kein Login)
    """
    print("\n📡 Scrape Reddit r/conspiracy...")
    
    url = "https://old.reddit.com/r/conspiracy/top.json?limit=100"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    posts = []
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            for post in data['data']['children']:
                title = post['data']['title']
                selftext = post['data'].get('selftext', '')
                
                # Titel
                if len(title) > 10 and len(title) < 200:
                    posts.append(clean_text(title))
                
                # Erste Zeile des Posts
                if selftext:
                    lines = selftext.split('\n')
                    for line in lines[:3]:
                        line = clean_text(line)
                        if len(line) > 20 and len(line) < 200:
                            posts.append(line)
                            break
            
            print(f"   ✅ {len(posts)} Posts gefunden")
        else:
            print(f"   ❌ HTTP {response.status_code}")
    
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    return posts


def scrape_4chan_x():
    """
    Scraped 4chan /x/ (Paranormal Board)
    ACHTUNG: Kann NSFW content enthalten, nur Threads-Titles nehmen
    """
    print("\n📡 Scrape 4chan /x/ (Paranormal)...")
    
    url = "https://a.4cdn.org/x/catalog.json"
    
    threads = []
    
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            for page in data:
                for thread in page.get('threads', []):
                    # Nur Subject/Topic nehmen (sicherer)
                    subject = thread.get('sub', '')
                    comment = thread.get('com', '')
                    
                    if subject:
                        subject = clean_text(subject)
                        subject = re.sub(r'<.*?>', '', subject)
                        if len(subject) > 10 and len(subject) < 150:
                            threads.append(subject)
            
            print(f"   ✅ {len(threads)} Threads gefunden")
        else:
            print(f"   ❌ HTTP {response.status_code}")
    
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    return threads


def create_extended_manual_dataset():
    """
    Erweiterter manueller Datensatz
    Mehr und vielfältigere Conspiracy-Phrasen
    """
    
    conspiracy_data = [
        # Klassische Conspiracy Phrasen
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
        
        # Verschwörungstheoretiker Klassiker
        "Die Chemtrails sind überall.",
        "Die Erde ist nicht rund.",
        "Die Echsenmenschen regieren uns.",
        "Niemand war auf dem Mond.",
        "Das wurde in einem Studio gefilmt.",
        "Die Illuminati stecken dahinter.",
        "Die neue Weltordnung kommt.",
        "Das ist Teil des großen Plans.",
        "Sie wollen uns alle chippen.",
        "5G macht uns krank.",
        
        # Typische Argumentationsmuster
        "Cui bono? Wer profitiert davon?",
        "Das passt zu perfekt zusammen.",
        "Die Timeline ist verdächtig.",
        "Zu viele Zufälle.",
        "Das ergibt keinen Sinn.",
        "Sie halten uns für dumm.",
        "Das Muster ist eindeutig.",
        "Verbindet die Punkte!",
        "Schaut hinter den Vorhang.",
        "Die Zeichen sind überall.",
        
        # Aufforderungen
        "Öffnet eure Augen!",
        "Denkt selbst nach!",
        "Hinterfragt alles!",
        "Informiert euch selbst!",
        "Lasst euch nicht täuschen!",
        "Glaubt nicht alles blind.",
        "Recherchiert selbst!",
        "Wacht endlich auf!",
        
        # Behauptungen über "Die"
        "Sie lügen uns an.",
        "Sie verstecken die Wahrheit.",
        "Sie haben Angst.",
        "Sie verlieren die Kontrolle.",
        "Sie wollen uns spalten.",
        "Sie fürchten uns.",
        "Sie können es nicht mehr verstecken.",
        "Sie unterschätzen das Volk.",
        
        # Über "die Wahrheit"
        "Die Wahrheit kommt ans Licht.",
        "Die Wahrheit ist da draußen.",
        "Die Wahrheit wird siegen.",
        "Die Wahrheit lässt sich nicht unterdrücken.",
        "Die Wahrheit ist offensichtlich.",
        "Die Wahrheit liegt auf der Hand.",
        
        # Mysteriöse Aussagen
        "Das ist größer als ihr denkt.",
        "Das ist erst der Anfang.",
        "Bald wird alles klar sein.",
        "Es kommt alles raus.",
        "Die Zeit ist nah.",
        "Das Kartenhaus fällt bald.",
        "Der Sturm kommt.",
        "Nichts ist wie es scheint.",
        
        # Über Medien
        "Die Medien lügen.",
        "Das wird zensiert.",
        "Mainstream Propaganda.",
        "Die Presse ist gekauft.",
        "Fake News überall.",
        "Kontrollierte Opposition.",
        "Gelenkte Berichterstattung.",
        
        # Pseudo-wissenschaftlich
        "Die Studien wurden manipuliert.",
        "Die Daten sprechen für sich.",
        "Die Zahlen lügen nicht.",
        "Die Beweise sind eindeutig.",
        "Die Fakten werden ignoriert.",
        "Die Wissenschaft wird unterdrückt.",
        
        # Über "das System"
        "Das System ist korrupt.",
        "Das System bröckelt.",
        "Das System fürchtet uns.",
        "Das System kollabiert.",
        "Das System lügt.",
        
        # Gruppenzugehörigkeit
        "Wir sind nicht allein.",
        "Immer mehr wachen auf.",
        "Die Menschen erkennen es.",
        "Wir sind die Mehrheit.",
        "Zusammen sind wir stark.",
        
        # Dramatische Wendungen
        "Es geht um alles.",
        "Es ist fünf vor zwölf.",
        "Wir haben keine Zeit mehr.",
        "Jetzt oder nie.",
        "Der Kampf hat begonnen.",
        
        # Klassische Verschwörungen
        "9/11 war ein Inside Job.",
        "JFK wurde ermordet von der CIA.",
        "Area 51 versteckt Aliens.",
        "Die Mondlandung war fake.",
        "Chemtrails vergiften uns.",
        "HAARP kontrolliert das Wetter.",
        "Reptilienmenschen unter uns.",
        "Die Bilderberger steuern alles.",
        
        # Neue Verschwörungen
        "5G aktiviert das Mikrochip.",
        "Bill Gates will uns alle impfen.",
        "Das Virus ist künstlich.",
        "Die Pandemie war geplant.",
        "Lockdowns sind Machtmissbrauch.",
        
        # Allgemeine Paranoia
        "Sie beobachten uns alle.",
        "Niemand ist sicher.",
        "Vertraut niemandem.",
        "Alles ist eine Lüge.",
        "Nichts ist real.",
        "Matrix überall.",
    ]
    
    return conspiracy_data


# HAUPT-SCRAPING
# ==============
print("=" * 70)
print("🚀 STARTE DATEN-SAMMLUNG")
print("=" * 70)
print()

all_data = []

# Methode 1: Reddit
print("Methode 1: Reddit r/conspiracy")
reddit_data = scrape_reddit_conspiracy()
all_data.extend(reddit_data)
time.sleep(2)

# Methode 2: 4chan (optional)
print("\nMethode 2: 4chan /x/")
print("⚠️  Möchtest du 4chan scrapen? (kann NSFW sein)")
user_choice = input("   4chan scrapen? (y/n): ").lower()
if user_choice == 'y':
    chan_data = scrape_4chan_x()
    all_data.extend(chan_data)
    time.sleep(2)
else:
    print("   ⏭️  Übersprungen")

# Methode 3: Manueller Datensatz
print("\nMethode 3: Erweiterter manueller Datensatz")
manual_data = create_extended_manual_dataset()
all_data.extend(manual_data)
print(f"   ✅ {len(manual_data)} manuelle Einträge")

print()
print("=" * 70)
print(f"✅ GESAMT: {len(all_data)} Einträge")
print("=" * 70)
print()

# Duplikate entfernen
all_data = list(set(all_data))
print(f"🧹 Nach Deduplizierung: {len(all_data)} einzigartig")
print()


# Speichern
# =========
if len(all_data) > 0:
    print("💾 Speichere...")
    
    with open('conspiracy_training_data.txt', 'w', encoding='utf-8') as f:
        for entry in all_data:
            f.write(entry + '\n')
    
    print("✅ conspiracy_training_data.txt")
    
    # JSON
    data_json = {
        'created_at': datetime.now().isoformat(),
        'type': 'conspiracy_theories',
        'sources': ['reddit', 'manual', '4chan (optional)'],
        'total': len(all_data),
        'entries': all_data
    }
    
    with open('conspiracy_training_data.json', 'w', encoding='utf-8') as f:
        json.dump(data_json, f, indent=2, ensure_ascii=False)
    
    print("✅ conspiracy_training_data.json")
    
    # Statistiken
    print()
    print("=" * 70)
    print("📊 STATISTIKEN")
    print("=" * 70)
    print(f"Einträge: {len(all_data)}")
    print(f"Zeichen: {sum(len(e) for e in all_data)}")
    print(f"Ø Länge: {sum(len(e) for e in all_data) / len(all_data):.1f}")
    
    # Beispiele
    print()
    print("📝 BEISPIELE:")
    print("-" * 70)
    for i, entry in enumerate(all_data[:20], 1):
        print(f"{i}. {entry}")
    print("-" * 70)

print()
print("=" * 70)
print("✅ FERTIG!")
print("=" * 70)
print()
print("Nächster Schritt: python conspiracy_train.py")
