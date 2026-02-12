"""
FINN v2 - Text Generierung (Word-Level)
========================================
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import pickle
import sys

print("=" * 70)
print("FINN v2 - TEXT GENERIERUNG (Word-Level)")
print("=" * 70)
print()


# Lade Modell und Tokenizer
# ==========================
print("📂 Lade Modell und Tokenizer...\n")

try:
    model = keras.models.load_model('finn_v2_model.keras')
    print("✅ Modell geladen")
except:
    print("❌ Modell nicht gefunden!")
    print("   Laufe erst: python finn_v2_train.py")
    sys.exit(1)

try:
    with open('tokenizer.pickle', 'rb') as f:
        tokenizer = pickle.load(f)
    print("✅ Tokenizer geladen")
except:
    print("❌ Tokenizer nicht gefunden!")
    sys.exit(1)

try:
    with open('max_sequence_len.txt', 'r') as f:
        max_sequence_len = int(f.read().strip())
    print(f"✅ Max Sequence Length: {max_sequence_len}")
except:
    print("❌ max_sequence_len.txt nicht gefunden!")
    sys.exit(1)

print()


# Text-Generierungs-Funktion
# ===========================
def generate_text(seed_text, next_words=10, temperature=1.0):
    """
    Generiert Text Wort fuer Wort

    WORD-LEVEL GENERIERUNG:
    =======================

    1. Nimm Seed-Text: "Was willst"
    2. Tokenisiere: [5, 12]
    3. Padding: [0, 0, 0, ..., 5, 12]
    4. FINN vorhersagt naechstes Wort: "du" (ID: 3)
    5. Fuege hinzu: "Was willst du"
    6. Wiederhole!

    TEMPERATURE:
    - 0.5 = konservativ (nimmt wahrscheinlichste Woerter)
    - 1.0 = balanced
    - 1.5 = kreativ (experimentiert mehr)
    """

    print(f"Seed: '{seed_text}'")
    print(f"Temperature: {temperature}")
    print(f"\nFINN sagt:")
    print("-" * 70)
    print(seed_text, end=' ')

    for _ in range(next_words):
        # Tokenisiere aktuellen Text
        token_list = tokenizer.texts_to_sequences([seed_text])[0]

        # Padding
        token_list = tf.keras.preprocessing.sequence.pad_sequences(
            [token_list],
            maxlen=max_sequence_len - 1,
            padding='pre'
        )

        # Vorhersage
        predictions = model.predict(token_list, verbose=0)[0]

        # Temperature Sampling
        predictions = np.log(predictions + 1e-7) / temperature
        exp_preds = np.exp(predictions)
        predictions = exp_preds / np.sum(exp_preds)

        # Sample naechstes Wort
        predicted_index = np.random.choice(len(predictions), p=predictions)

        # Finde das Wort
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                output_word = word
                break

        if output_word:
            seed_text += " " + output_word
            print(output_word, end=' ', flush=True)

    print()
    print("-" * 70)
    return seed_text


# BEISPIELE
# =========
print("=" * 70)
print("BEISPIELE:")
print("=" * 70)
print()

print("1️⃣  Konservativ (temperature=0.5)")
result1 = generate_text("Was", next_words=15, temperature=0.5)
print()

print("2️⃣  Balanced (temperature=1.0)")
result2 = generate_text("Schon wieder", next_words=15, temperature=1.0)
print()

print("3️⃣  Kreativ (temperature=1.5)")
result3 = generate_text("Muss das", next_words=15, temperature=1.5)
print()


# INTERAKTIVER MODUS
# ==================
print("=" * 70)
print("🎮 INTERAKTIVER MODUS")
print("=" * 70)
print()
print("Gib einen Starttext ein (oder 'quit' zum Beenden)")
print("Commands:")
print("  /temp 0.5  - Setze temperature auf 0.5")
print("  /words 20  - Generiere 20 Woerter")
print()

current_temp = 1.0
current_words = 10

while True:
    user_input = input("\nDu: ").strip()

    if user_input.lower() in ['quit', 'exit', 'q']:
        print("\nFINN: 'Endlich... 🙄'")
        break

    # Commands
    if user_input.startswith('/temp '):
        try:
            current_temp = float(user_input.split()[1])
            print(f"✅ Temperature auf {current_temp} gesetzt")
        except:
            print("❌ Ungueltige temperature")
        continue

    if user_input.startswith('/words '):
        try:
            current_words = int(user_input.split()[1])
            print(f"✅ Anzahl Woerter auf {current_words} gesetzt")
        except:
            print("❌ Ungueltige Anzahl")
        continue

    if len(user_input) == 0:
        print("FINN: 'Du musst schon was schreiben... *seufz*'")
        continue

    print("\nFINN: ", end='')
    response = generate_text(
        user_input,
        next_words=current_words,
        temperature=current_temp
    )


print("\n" + "=" * 70)
print("FERTIG!")
print("=" * 70)
