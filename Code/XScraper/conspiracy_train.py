"""
CONSPIRACY FINN - Training
===========================

Trainiert FINN auf Verschwörungstheorien
Für maximale Unterhaltung 🛸👽🔺
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

print("=" * 70)
print("🛸 CONSPIRACY FINN - TRAINING 🛸")
print("=" * 70)
print()
print("⚠️  WARNUNG: Dieser Bot wird Verschwörungstheorien generieren!")
print("   Nur für Entertainment-Zwecke!")
print()


# Daten laden
# ===========
print("📂 Lade Conspiracy Trainingsdaten...\n")

try:
    with open('conspiracy_training_data.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"✅ {len(text)} Zeichen geladen")
except FileNotFoundError:
    print("❌ conspiracy_training_data.txt nicht gefunden!")
    print("   Laufe erst: python conspiracy_scraper.py")
    exit()

# Sätze aufteilen
sentences = text.split('\n')
sentences = [s.strip() for s in sentences if s.strip()]
print(f"✅ {len(sentences)} Conspiracy-Statements gefunden\n")

# Beispiele anzeigen
print("📝 BEISPIEL-DATEN:")
print("-" * 70)
for i, s in enumerate(sentences[:5], 1):
    print(f"{i}. {s}")
print("-" * 70)
print()


# Tokenisierung
# =============
print("🔤 Tokenisierung...\n")

tokenizer = Tokenizer(
    filters='',
    lower=True,
    oov_token='<UNK>'
)

tokenizer.fit_on_texts(sentences)
total_words = len(tokenizer.word_index) + 1

print(f"✅ Vokabular: {total_words} Wörter")
print(f"\nTop Conspiracy Wörter:")
for word, idx in list(tokenizer.word_index.items())[:20]:
    print(f"   '{word}' → {idx}")
print()


# Sequenzen erstellen
# ===================
print("📝 Erstelle Trainings-Sequenzen...\n")

input_sequences = []

for sentence in sentences:
    token_list = tokenizer.texts_to_sequences([sentence])[0]
    
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

print(f"✅ {len(input_sequences)} Trainingsbeispiele")

max_sequence_len = max([len(seq) for seq in input_sequences])
print(f"✅ Max Sequenz-Länge: {max_sequence_len}")

input_sequences = np.array(pad_sequences(
    input_sequences,
    maxlen=max_sequence_len,
    padding='pre'
))

X = input_sequences[:, :-1]
y = input_sequences[:, -1]
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

print(f"✅ X shape: {X.shape}")
print(f"✅ y shape: {y.shape}\n")


# Modell bauen
# ============
print("🧠 Baue CONSPIRACY FINN...\n")

"""
CONSPIRACY FINN ARCHITEKTUR:
- Größeres Embedding (mehr "verrückte" Kombinationen)
- Mehr LSTM Units (komplexere Conspiracy-Muster)
- Höheres Dropout (gegen Overfitting bei wirren Texten)
"""

model = keras.Sequential([
    # Größeres Embedding für kreativere Kombinationen
    layers.Embedding(
        input_dim=total_words,
        output_dim=150,  # Größer als vorher!
        input_length=max_sequence_len - 1
    ),
    
    # Zwei LSTM Layers für komplexere Muster
    layers.LSTM(200, return_sequences=True),  # Erster Layer
    layers.Dropout(0.3),
    
    layers.LSTM(200, return_sequences=False),  # Zweiter Layer
    layers.Dropout(0.3),
    
    # Output
    layers.Dense(total_words, activation='softmax')
])

print("✅ Modell-Architektur:")
print("-" * 70)
model.summary()
print("-" * 70)
print()


# Kompilieren
# ===========
print("⚙️  Kompiliere...\n")

model.compile(
    loss='categorical_crossentropy',
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    metrics=['accuracy']
)

print("✅ Modell bereit!\n")


# Training
# ========
print("=" * 70)
print("🚀 TRAINING STARTET")
print("=" * 70)
print()
print("⏰ Das kann 10-20 Minuten dauern (größeres Modell)...")
print()

history = model.fit(
    X, y,
    epochs=150,  # Mehr Epochen für bessere Conspiracy-Qualität
    batch_size=64,
    verbose=1,
    validation_split=0.1
)

print()
print("=" * 70)
print("✅ TRAINING ABGESCHLOSSEN!")
print("=" * 70)
print()


# Speichern
# =========
print("💾 Speichere CONSPIRACY FINN...\n")

model.save('conspiracy_finn_model.keras')
print("✅ Modell: conspiracy_finn_model.keras")

with open('conspiracy_tokenizer.pickle', 'wb') as f:
    pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)
print("✅ Tokenizer: conspiracy_tokenizer.pickle")

with open('conspiracy_max_seq_len.txt', 'w') as f:
    f.write(str(max_sequence_len))
print("✅ Max Seq Len gespeichert")
print()


# Statistiken
# ===========
print("=" * 70)
print("📊 TRAINING-STATISTIKEN")
print("=" * 70)
print(f"Finale Loss: {history.history['loss'][-1]:.4f}")
print(f"Finale Accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Val Loss: {history.history['val_loss'][-1]:.4f}")
print(f"Val Accuracy: {history.history['val_accuracy'][-1]:.4f}")
print()

print("=" * 70)
print("🎉 CONSPIRACY FINN IST BEREIT!")
print("=" * 70)
print()
print("⚠️  DISCLAIMER: Dieser Bot generiert Satire/Parodie!")
print("   Verschwörungstheorien sind nicht faktisch!")
print()
print("Nächster Schritt:")
print("  python conspiracy_generate.py")
