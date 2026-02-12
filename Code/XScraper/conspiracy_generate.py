"""
CONSPIRACY FINN - Generator
============================

Lässt CONSPIRACY FINN wilde Theorien generieren 🛸
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import pickle
import sys
import random

print("=" * 70)
print("🛸 CONSPIRACY FINN - GENERATOR 🛸")
print("=" * 70)
print()
print("⚠️  ACHTUNG: Satire/Parodie! Nicht ernst nehmen!")
print()


# Laden
# =====
print("📂 Lade CONSPIRACY FINN...\n")

try:
    model = keras.models.load_model('conspiracy_finn_model.keras')
    print("✅ Modell geladen")
except:
    print("❌ Modell nicht gefunden!")
    print("   Laufe erst: python conspiracy_train.py")
    sys.exit(1)

try:
    with open('conspiracy_tokenizer.pickle', 'rb') as f:
        tokenizer = pickle.load(f)
    print("✅ Tokenizer geladen")
except:
    print("❌ Tokenizer nicht gefunden!")
    sys.exit(1)

try:
    with open('conspiracy_max_seq_len.txt', 'r') as f:
        max_sequence_len = int(f.read().strip())
    print(f"✅ Max Sequence Length: {max_sequence_len}")
except:
    print("❌ Max sequence length nicht gefunden!")
    sys.exit(1)

print()


# Generator
# =========
def generate_conspiracy(seed_text, next_words=20, temperature=1.2):
    """
    Generiert Verschwörungstheorien
    
    Temperature 1.2-1.5 = Optimal für wirre Theorien!
    """
    
    print(f"🔺 Seed: '{seed_text}'")
    print(f"🌡️  Temperature: {temperature}")
    print()
    print("CONSPIRACY FINN sagt:")
    print("-" * 70)
    print(seed_text, end=' ')
    
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = tf.keras.preprocessing.sequence.pad_sequences(
            [token_list],
            maxlen=max_sequence_len - 1,
            padding='pre'
        )
        
        predictions = model.predict(token_list, verbose=0)[0]
        
        # Temperature Sampling (höher = wilder)
        predictions = np.log(predictions + 1e-7) / temperature
        exp_preds = np.exp(predictions)
        predictions = exp_preds / np.sum(exp_preds)
        
        predicted_index = np.random.choice(len(predictions), p=predictions)
        
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
    print()
    return seed_text


# Zufällige Conspiracy Seeds
# ===========================
CONSPIRACY_SEEDS = [
    "Die Wahrheit",
    "Sie wollen",
    "Das ist",
    "Wacht auf",
    "Die Elite",
    "Niemand",
    "Alles ist",
    "Das System",
    "Sie kontrollieren",
    "Die Medien",
    "Glaubt nicht",
    "Das wurde",
    "Folgt der",
    "Die verstecken",
    "Zufall",
]


# BEISPIELE
# =========
print("=" * 70)
print("🎪 BEISPIEL-CONSPIRACY-THEORIEN")
print("=" * 70)
print()
print("⚠️  SATIRE! Nicht ernst nehmen!\n")

for i in range(5):
    seed = random.choice(CONSPIRACY_SEEDS)
    temp = random.uniform(1.1, 1.5)
    
    print(f"\n{'='*70}")
    print(f"THEORIE #{i+1}")
    print('='*70)
    
    result = generate_conspiracy(
        seed,
        next_words=25,
        temperature=temp
    )
    
    print()


# INTERAKTIV
# ==========
print()
print("=" * 70)
print("🎮 INTERAKTIVER MODUS")
print("=" * 70)
print()
print("Gib einen Starttext ein (oder 'quit' zum Beenden)")
print()
print("Commands:")
print("  /temp <wert>   - Setze temperature (1.0-2.0)")
print("  /words <zahl>  - Anzahl Wörter")
print("  /random        - Zufällige Theorie")
print()

current_temp = 1.3
current_words = 20

while True:
    user_input = input("\n🔺 Seed: ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("\nCONSPIRACY FINN: 'Die Wahrheit wird siegen... 🛸'")
        break
    
    # Commands
    if user_input.startswith('/temp '):
        try:
            current_temp = float(user_input.split()[1])
            current_temp = max(0.5, min(2.0, current_temp))
            print(f"✅ Temperature: {current_temp}")
        except:
            print("❌ Ungültig")
        continue
    
    if user_input.startswith('/words '):
        try:
            current_words = int(user_input.split()[1])
            print(f"✅ Wörter: {current_words}")
        except:
            print("❌ Ungültig")
        continue
    
    if user_input == '/random':
        user_input = random.choice(CONSPIRACY_SEEDS)
        print(f"🎲 Zufälliger Seed: '{user_input}'")
    
    if len(user_input) == 0:
        print("FINN: 'Die Wahrheit braucht einen Anfang... 👽'")
        continue
    
    print()
    result = generate_conspiracy(
        user_input,
        next_words=current_words,
        temperature=current_temp
    )


print()
print("=" * 70)
print("FERTIG!")
print("=" * 70)
print()
print("⚠️  DISCLAIMER:")
print("   Dieser Bot ist reine Satire und Unterhaltung!")
print("   Verschwörungstheorien sind nicht faktisch!")
print("   Bitte kritisch denken! 🧠")
