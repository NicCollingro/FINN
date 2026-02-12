"""
FINN v2 - Word-Level RNN
========================

WARUM WORD-LEVEL BESSER IST:
- Lernt Wort-Kombinationen statt Buchstaben
- Braucht weniger Sequenz-Laenge
- Generiert sinnvollere Saetze
- Schneller beim Training

CHARACTER-LEVEL: "W-a-s- -w-i-l-l-s-t- -d-u"
WORD-LEVEL:      "Was willst du"
→ Viel effizienter!
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

print("=" * 70)
print("FINN v2 - WORD-LEVEL RNN")
print("=" * 70)
print()


# SCHRITT 1: Daten laden
# ======================
print("📂 Lade Trainingsdaten...\n")

try:
    with open('finn_training_data.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"✅ {len(text)} Zeichen geladen")
except FileNotFoundError:
    print("⚠️  finn_training_data.txt nicht gefunden!")
    print("   Laufe erst: python create_dataset.py")
    exit()

# Saetze aufteilen
sentences = text.split('\n')
sentences = [s.strip() for s in sentences if s.strip()]
print(f"✅ {len(sentences)} Saetze gefunden\n")


# SCHRITT 2: Tokenisierung (Woerter → Zahlen)
# ============================================
print("🔤 Tokenisierung (Woerter zu Zahlen)...\n")

"""
TOKENIZER:
- Baut ein Vokabular aus allen Woertern
- Weist jedem Wort eine Nummer zu
- Wandelt Saetze in Zahlen-Sequenzen um

Beispiel:
"Was willst du" → [5, 12, 3]
"""

tokenizer = Tokenizer(
    filters='',  # Behalte Interpunktion
    lower=True,  # Kleinbuchstaben
    oov_token='<UNK>'  # Token fuer unbekannte Woerter
)

tokenizer.fit_on_texts(sentences)
total_words = len(tokenizer.word_index) + 1  # +1 fuer padding

print(f"✅ Vokabular-Groesse: {total_words} Woerter")
print(f"\nBeispiel Woerter und ihre IDs:")
for word, idx in list(tokenizer.word_index.items())[:10]:
    print(f"   '{word}' → {idx}")


# SCHRITT 3: Sequenzen erstellen
# ===============================
print(f"\n📝 Erstelle Trainings-Sequenzen...\n")

"""
INPUT-OUTPUT PAARE:
===================

Aus dem Satz "Was willst du diesmal"
Machen wir mehrere Trainingsbeispiele:

Input: [Was]              → Output: [willst]
Input: [Was, willst]      → Output: [du]
Input: [Was, willst, du]  → Output: [diesmal]

So lernt FINN Wort-fuer-Wort vorherzusagen!
"""

input_sequences = []

for sentence in sentences:
    token_list = tokenizer.texts_to_sequences([sentence])[0]

    # Erstelle n-grams
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

print(f"✅ {len(input_sequences)} Trainingsbeispiele erstellt")

# Finde maximale Sequenzlaenge
max_sequence_len = max([len(seq) for seq in input_sequences])
print(f"✅ Max Sequenz-Laenge: {max_sequence_len} Woerter")

# Padding: Alle Sequenzen auf gleiche Laenge bringen
input_sequences = np.array(pad_sequences(
    input_sequences,
    maxlen=max_sequence_len,
    padding='pre'  # Fuege Nullen am Anfang ein
))

print(f"✅ Sequenzen gepaddet auf Form: {input_sequences.shape}")

# X = Input (alle Woerter ausser das letzte)
# y = Output (das letzte Wort als One-Hot)
X = input_sequences[:, :-1]
y = input_sequences[:, -1]

# One-Hot Encoding fuer Output
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

print(f"\n✅ X shape: {X.shape} (Input)")
print(f"✅ y shape: {y.shape} (Output)")


# SCHRITT 4: Modell bauen
# ========================
print("\n🧠 Baue FINN v2 Modell...\n")

"""
WORD-LEVEL RNN ARCHITEKTUR:
============================

1. EMBEDDING LAYER:
   - Wandelt Wort-IDs in dense Vektoren um
   - Dimension: 100
   - Beispiel: Wort 5 → [0.2, -0.5, 0.1, ...]
   - Woerter mit aehnlicher Bedeutung bekommen aehnliche Vektoren!

2. LSTM LAYER:
   - 150 Neuronen
   - Verarbeitet die Wort-Sequenz
   - Merkt sich Kontext

3. DENSE LAYER:
   - Output: Wahrscheinlichkeit fuer jedes Wort
"""

model = keras.Sequential([
    # Embedding: Wort-ID → Vektor
    layers.Embedding(
        input_dim=total_words,
        output_dim=100,  # Jedes Wort wird zu 100-dim Vektor
        input_length=max_sequence_len - 1
    ),

    # LSTM mit mehr Neuronen als vorher
    layers.LSTM(150, return_sequences=False),

    # Dropout gegen Overfitting
    layers.Dropout(0.2),

    # Dense Output Layer
    layers.Dense(total_words, activation='softmax')
])

print("✅ Modell-Architektur:")
print("-" * 70)
model.summary()
print("-" * 70)


# SCHRITT 5: Kompilieren
# ======================
print("\n⚙️  Kompiliere Modell...\n")

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

print("✅ Modell bereit!")


# SCHRITT 6: Training
# ===================
print("\n🚀 TRAINING STARTET")
print("=" * 70)
print()

history = model.fit(
    X, y,
    epochs=100,  # Mehr Epochen weil wir mehr Daten haben
    batch_size=32,
    verbose=1,
    validation_split=0.1  # 10% fuer Validierung
)

print("\n" + "=" * 70)
print("✅ TRAINING ABGESCHLOSSEN!")
print("=" * 70)


# SCHRITT 7: Speichern
# ====================
print("\n💾 Speichere Modell und Tokenizer...\n")

model.save('finn_v2_model.keras')
print("✅ Modell gespeichert: finn_v2_model.keras")

# Tokenizer speichern (brauchen wir fuer Text-Generierung!)
with open('tokenizer.pickle', 'wb') as f:
    pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)
print("✅ Tokenizer gespeichert: tokenizer.pickle")

# Max Sequence Length speichern
with open('max_sequence_len.txt', 'w') as f:
    f.write(str(max_sequence_len))
print("✅ Max Sequence Length gespeichert")


# STATISTIKEN
print("\n📊 Training-Statistiken:")
print(f"   Finale Loss: {history.history['loss'][-1]:.4f}")
print(f"   Finale Accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"   Val Loss: {history.history['val_loss'][-1]:.4f}")
print(f"   Val Accuracy: {history.history['val_accuracy'][-1]:.4f}")

print("\n" + "=" * 70)
print("🎉 FINN v2 IST BEREIT!")
print("=" * 70)
print("\nNaechster Schritt: python finn_v2_generate.py")
