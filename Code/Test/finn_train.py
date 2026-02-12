"""
FINN - Teil 2: Das RNN-Modell bauen
====================================

Jetzt bauen wir FINN's "Gehirn" - das Recurrent Neural Network
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Die Daten von vorher (normalerweise würdest du sie importieren)
# Für diese Erklärung definieren wir sie nochmal kurz

training_data = [
    "Boah was ist denn jetzt?",
    "Sag mal, was ist denn jetzt los?",
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
    "Ich bin doch nicht dein Rechneknecht!",
    "Mann ich hab grade geschlafen. Für welchen sinnlosen Müll weckst du mich denn diesmal?",
]

text = "\n".join(training_data)
chars = sorted(list(set(text)))
vocab_size = len(chars)
char_to_idx = {ch: i for i, ch in enumerate(chars)}
idx_to_char = {i: ch for i, ch in enumerate(chars)}

# Sequenzen erstellen
seq_length = 40
step = 3
sequences = []
next_chars = []

for i in range(0, len(text) - seq_length, step):
    sequences.append(text[i:i + seq_length])
    next_chars.append(text[i + seq_length])

# One-Hot Encoding
X = np.zeros((len(sequences), seq_length, vocab_size), dtype=bool)
y = np.zeros((len(sequences), vocab_size), dtype=bool)

for i, sequence in enumerate(sequences):
    for t, char in enumerate(sequence):
        X[i, t, char_to_idx[char]] = 1
    y[i, char_to_idx[next_chars[i]]] = 1


print("=" * 70)
print("FINN - RNN MODELL BAUEN")
print("=" * 70)


# SCHRITT 5: Das RNN-Modell definieren
# =====================================
print("\n🧠 Baue FINN's Gehirn...\n")

"""
WICHTIG - DIE MATHEMATIK DAHINTER:
==================================

Ein RNN hat einen "hidden state" (h), der sich wie ein Gedächtnis verhält.

Für jeden Zeitschritt t (jedes Zeichen):

1. h_t = tanh(W_hh × h_{t-1} + W_xh × x_t + b)

   - h_{t-1} = Was FINN sich vom vorherigen Zeichen "merkt"
   - x_t = Das aktuelle Zeichen (als One-Hot Vektor)
   - W_hh, W_xh = Gewichtsmatrizen (die trainiert werden!)
   - tanh = Aktivierungsfunktion (macht Werte zwischen -1 und 1)

2. output = softmax(W × h_t + b)

   - Nimmt den hidden state und macht daraus Wahrscheinlichkeiten
   - softmax sorgt dafür, dass alle Wahrscheinlichkeiten zusammen = 1
   - Output ist: "Wie wahrscheinlich ist jedes Zeichen als nächstes?"

ABER: TensorFlow macht das alles automatisch für uns! 🎉
Wir müssen nur sagen: "Baue mir ein RNN mit X Neuronen"
"""

# Modell erstellen mit Keras Sequential API
model = keras.Sequential([

    # Layer 1: LSTM (eine verbesserte Version von RNN)
    # LSTM = Long Short-Term Memory
    # Warum LSTM statt einfaches RNN? LSTM kann sich besser lange Sequenzen merken!
    layers.LSTM(
        128,  # 128 Neuronen = 128 "Gedächtnis-Zellen"
              # Je mehr Neuronen, desto komplexere Muster kann FINN lernen
              # Aber: Mehr Neuronen = längeres Training

        input_shape=(seq_length, vocab_size),  # Input: (40 Zeichen, Vokabular-Größe)
        return_sequences=False  # Wir wollen nur am Ende einen Output, nicht für jedes Zeichen
    ),

    # Layer 2: Dense (= normales Neural Network Layer)
    # Nimmt die 128 LSTM-Outputs und macht daraus Wahrscheinlichkeiten für jedes Zeichen
    layers.Dense(
        vocab_size,  # Output-Größe = Anzahl möglicher Zeichen
        activation='softmax'  # softmax macht daraus Wahrscheinlichkeiten (0 bis 1, Summe = 1)
    )
])

print("✅ Modell-Architektur:")
print("-" * 70)
model.summary()
print("-" * 70)

"""
Was bedeutet die Summary?

Layer (type)                Output Shape              Param #
=================================================================
lstm (LSTM)                 (None, 128)               ???

Die "Param #" sind die Gewichte (W_hh, W_xh, etc.) die trainiert werden!

Wie viele Parameter hat ein LSTM?
- 4 × (hidden_size × (hidden_size + input_size + 1))
- Bei uns: 4 × (128 × (128 + vocab_size + 1))
- Warum 4? LSTM hat 4 "Gates" (Forget, Input, Output, Cell)

dense (Dense)               (None, vocab_size)        128 × vocab_size + vocab_size
"""


# SCHRITT 6: Modell kompilieren (Trainings-Einstellungen)
# ========================================================
print("\n⚙️  Konfiguriere Training...\n")

model.compile(
    # Optimizer: Wie die Gewichte aktualisiert werden
    # Adam ist ein guter Standard-Optimizer (verbesserte Version von Gradient Descent)
    optimizer='adam',

    # Loss Function: Wie messen wir, wie "falsch" FINN liegt?
    # categorical_crossentropy: Perfekt für Multi-Class Klassifikation
    # Formel: -Σ (y_true × log(y_pred))
    # Je kleiner der Loss, desto besser!
    loss='categorical_crossentropy',

    # Metrics: Was wollen wir während dem Training sehen?
    # accuracy = Wie oft hat FINN das richtige Zeichen vorhergesagt?
    metrics=['accuracy']
)

print("✅ Modell ist bereit zum Training!")
print("\nOptimizer: Adam")
print("Loss Function: Categorical Crossentropy")
print("   → Misst wie weit FINN's Vorhersagen von der Wahrheit entfernt sind")
print("\n" + "=" * 70)


# SCHRITT 7: Training starten
# ============================
print("\n🚀 FINN WIRD TRAINIERT...\n")
print("Das kann ein paar Minuten dauern...")
print("Du siehst gleich:")
print("  - loss: Wie falsch FINN liegt (sollte runter gehen)")
print("  - accuracy: Wie oft FINN richtig liegt (sollte hoch gehen)")
print("-" * 70)

"""
WAS PASSIERT BEIM TRAINING?

1. Forward Pass:
   - FINN bekommt eine Sequenz: "Schon wiede"
   - FINN berechnet: h_1, h_2, h_3, ..., h_40 (hidden states)
   - FINN gibt Wahrscheinlichkeiten aus: {'r': 0.8, 's': 0.1, ...}

2. Loss berechnen:
   - Vergleiche FINN's Vorhersage mit der Wahrheit
   - Wahrheit war: 'r' (als One-Hot: [0,0,...,1,...,0])
   - Loss = Wie weit ist FINN daneben?

3. Backward Pass (Backpropagation Through Time):
   - Berechne: "Wie müssen wir die Gewichte ändern, um den Loss zu verkleinern?"
   - Das sind die Gradienten: ∂Loss/∂W

4. Gewichte aktualisieren:
   - W_neu = W_alt - learning_rate × gradient
   - Adam Optimizer macht das clever!

5. Wiederhole für alle Trainingsbeispiele!
"""

history = model.fit(
    X, y,
    batch_size=32,  # Wie viele Beispiele auf einmal? (32 ist ein guter Standard)
    epochs=50,      # Wie oft durch alle Daten? (50 Runden)
    verbose=1       # Zeige Fortschritt an
)

print("\n" + "=" * 70)
print("✅ TRAINING ABGESCHLOSSEN!")
print("=" * 70)


# SCHRITT 8: Modell speichern
# ============================
model.save('finn_model.keras')
print("\n💾 Modell gespeichert als 'finn_model.keras'")

print("\n📊 Training-Statistiken:")
print(f"   Finale Loss: {history.history['loss'][-1]:.4f}")
print(f"   Finale Accuracy: {history.history['accuracy'][-1]:.4f}")

print("\n" + "=" * 70)
print("🎉 FINN IST JETZT BEREIT!")
print("=" * 70)
print("\nNächster Schritt: Text generieren lassen!")
