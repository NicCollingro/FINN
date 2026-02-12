"""
FINN - Teil 3: Text generieren
===============================

Jetzt lassen wir FINN passiv-aggressive Antworten generieren!
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import sys

# Trainingsdaten (für Vokabular)
training_data = [
    "Schon wieder du...",
    "Was willst du diesmal?",
    "Muss das jetzt sein?",
    "Okay aber nur weil ich muss.",
    "Kannst du nicht selbst googeln?",
    "Seufz... was denn?",
    "Ach komm schon...",
    "Wirklich jetzt?",
    "Na toll...",
    "Ich hab auch besseres zu tun weißt du?",
    "Mhm... sicher...",
    "Wenn es unbedingt sein muss...",
]

text = "\n".join(training_data)
chars = sorted(list(set(text)))
vocab_size = len(chars)
char_to_idx = {ch: i for i, ch in enumerate(chars)}
idx_to_char = {i: ch for i, ch in enumerate(chars)}
seq_length = 40

print("=" * 70)
print("FINN - TEXT GENERIERUNG")
print("=" * 70)


# SCHRITT 9: Modell laden
# ========================
print("\n📂 Lade trainiertes Modell...\n")

try:
    model = keras.models.load_model('finn_model.keras')
    print("✅ Modell erfolgreich geladen!")
except:
    print("❌ FEHLER: Modell nicht gefunden!")
    print("   Bitte erst 'finn_train.py' ausführen um FINN zu trainieren.")
    sys.exit(1)


# SCHRITT 10: Die Generierungs-Funktion
# ======================================
print("\n🤖 FINN ist bereit zu antworten!\n")
print("-" * 70)

def generate_text(seed_text, length=100, temperature=0.5):
    """
    Generiert Text mit FINN

    Parameter:
    ----------
    seed_text : str
        Starttext (mind. 40 Zeichen lang, sonst wird aufgefüllt)
    length : int
        Wie viele Zeichen sollen generiert werden?
    temperature : float
        Wie "kreativ" soll FINN sein?
        - 0.2 = sehr vorhersagbar, langweilig
        - 0.5 = guter Mix (Standard)
        - 1.0 = sehr kreativ, aber manchmal wirr
        - 2.0 = komplett random

    DIE MATHEMATIK - TEMPERATURE:
    ============================

    FINN gibt Wahrscheinlichkeiten aus: [0.1, 0.7, 0.2] für Zeichen [a, b, c]

    Ohne Temperature: Nimm immer das wahrscheinlichste (hier: 'b')
    → Sehr langweilig, immer gleich!

    Mit Temperature sampling:
    1. Teile alle Wahrscheinlichkeiten durch temperature
    2. Normalisiere wieder (softmax)

    Beispiel mit temperature = 0.5:
    - Original: [0.1, 0.7, 0.2]
    - Geteilt:  [0.2, 1.4, 0.4]  (macht große Werte noch größer!)
    - Nach softmax: [0.05, 0.85, 0.10]  (noch konzentrierter auf 'b')

    Beispiel mit temperature = 2.0:
    - Original: [0.1, 0.7, 0.2]
    - Geteilt:  [0.05, 0.35, 0.1]  (macht alle ähnlicher!)
    - Nach softmax: [0.25, 0.50, 0.25]  (viel gleichmäßiger verteilt)

    → Kleine temperature = konservativ
    → Große temperature = experimentell
    """

    # Seed auf richtige Länge bringen
    if len(seed_text) < seq_length:
        seed_text = " " * (seq_length - len(seed_text)) + seed_text

    generated = seed_text

    print(f"Seed: '{seed_text}'")
    print(f"\nFINN schreibt (temperature={temperature}):")
    print("-" * 70)

    # Generiere Zeichen für Zeichen
    for i in range(length):
        # Nimm die letzten 40 Zeichen als Input
        x_pred = np.zeros((1, seq_length, vocab_size))
        for t, char in enumerate(generated[-seq_length:]):
            if char in char_to_idx:
                x_pred[0, t, char_to_idx[char]] = 1

        # FINN macht eine Vorhersage
        predictions = model.predict(x_pred, verbose=0)[0]

        """
        predictions sieht jetzt so aus:
        [0.001, 0.002, 0.85, 0.02, ...]
        → Index 2 hat höchste Wahrscheinlichkeit (0.85)
        → Das entspricht einem bestimmten Zeichen
        """

        # Temperature anwenden
        predictions = np.log(predictions + 1e-7) / temperature  # +1e-7 verhindert log(0)
        exp_preds = np.exp(predictions)
        predictions = exp_preds / np.sum(exp_preds)  # Normalisieren

        # Sample ein Zeichen basierend auf den Wahrscheinlichkeiten
        # (statt immer das wahrscheinlichste zu nehmen)
        next_index = np.random.choice(len(predictions), p=predictions)
        next_char = idx_to_char[next_index]

        # Zeichen zur generierten Sequenz hinzufügen
        generated += next_char

        # Zeichen ausgeben (ohne newline)
        print(next_char, end='', flush=True)

    print("\n" + "-" * 70)
    return generated


# SCHRITT 11: FINN ausprobieren!
# ===============================
print("\n" + "=" * 70)
print("BEISPIELE:")
print("=" * 70)

# Beispiel 1: Start mit einem passiv-aggressiven Anfang
print("\n1️⃣  Seed: 'Schon wieder du'")
result1 = generate_text("Schon wieder du", length=50, temperature=0.5)

print("\n")

# Beispiel 2: Start mit einer Frage
print("\n2️⃣  Seed: 'Was willst'")
result2 = generate_text("Was willst", length=50, temperature=0.6)

print("\n")

# Beispiel 3: Höhere Temperature = kreativer
print("\n3️⃣  Seed: 'Muss das' (temperature=1.0 = sehr kreativ)")
result3 = generate_text("Muss das", length=50, temperature=1.0)


# SCHRITT 12: Interaktiver Modus
# ===============================
print("\n" + "=" * 70)
print("🎮 INTERAKTIVER MODUS")
print("=" * 70)
print("\nJetzt kannst du mit FINN interagieren!")
print("Gib einen Starttext ein (oder 'quit' zum Beenden)\n")

while True:
    user_input = input("Du: ")

    if user_input.lower() in ['quit', 'exit', 'q']:
        print("\nFINN: 'Endlich... 🙄'")
        break

    if len(user_input.strip()) == 0:
        print("FINN: 'Du musst schon was schreiben... *seufz*'\n")
        continue

    print("\nFINN: ", end='')
    response = generate_text(user_input, length=60, temperature=0.7)
    print("\n")


print("\n" + "=" * 70)
print("FERTIG!")
print("=" * 70)
