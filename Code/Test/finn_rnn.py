"""
FINN - Fundamentally Irascible Neural Network
Ein einfaches character-level RNN für passiv-aggressive Chatbot-Antworten

Wir fangen ganz einfach an: FINN lernt Zeichen für Zeichen (character-level)
anstatt Wort für Wort. Das macht die Mathematik überschaubarer.
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import random

print("=" * 50)
print("FINN - Fundamentally Irascible Neural Network")
print("=" * 50)


# SCHRITT 1: Trainingsdaten vorbereiten
# ======================================
# FINN braucht Beispiele für passiv-aggressive Antworten
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

# Alle Texte zu einem String zusammenfügen
text = "\n".join(training_data)
print(f"\nTrainingsdaten ({len(text)} Zeichen):")
print(text[:200] + "...")


# SCHRITT 2: Zeichen-Vokabular erstellen
# =======================================
# Wir brauchen ein Mapping: Zeichen → Zahl (für das Neural Network)
# Warum? Neural Networks verstehen nur Zahlen, keine Buchstaben!

chars = sorted(list(set(text)))  # Alle einzigartigen Zeichen
vocab_size = len(chars)

print(f"\nVokabular-Größe: {vocab_size} einzigartige Zeichen")
print(f"Zeichen: {chars}")

# Zwei Dictionaries für Hin- und Rückübersetzung
char_to_idx = {ch: i for i, ch in enumerate(chars)}  # 'a' → 0, 'b' → 1, ...
idx_to_char = {i: ch for i, ch in enumerate(chars)}  # 0 → 'a', 1 → 'b', ...

print("\nBeispiel Mappings:")
print(f"'S' → {char_to_idx['S']}")
print(f"{char_to_idx['S']} → '{idx_to_char[char_to_idx['S']]}'")


# SCHRITT 3: Trainingsdaten in Sequenzen aufteilen
# =================================================
# RNNs lernen: "Wenn ich diese Zeichen sehe, kommt als nächstes..."
# Wir erstellen Input-Output Paare:
# Input: "Schon wiede" → Output: "r"
# Input: "chon wieder" → Output: " "

seq_length = 40  # Wie viele Zeichen FINN auf einmal sieht
step = 3  # Wie viele Zeichen wir zwischen Sequenzen überspringen

sequences = []  # Input-Sequenzen
next_chars = []  # Das jeweils nächste Zeichen (= was FINN vorhersagen soll)

for i in range(0, len(text) - seq_length, step):
    sequences.append(text[i:i + seq_length])
    next_chars.append(text[i + seq_length])

print(f"\nAnzahl Trainingsbeispiele: {len(sequences)}")
print("\nBeispiel:")
print(f"Input:  '{sequences[0]}'")
print(f"Output: '{next_chars[0]}'")


# SCHRITT 4: Daten in Zahlen umwandeln (One-Hot Encoding)
# ========================================================
# One-Hot Encoding: Jedes Zeichen wird zu einem Vektor
# z.B. bei Vokabular [a,b,c]: 'b' → [0, 1, 0]

print("\nKonvertiere zu Zahlen (One-Hot Encoding)...")

# Erstelle leere Arrays
X = np.zeros((len(sequences), seq_length, vocab_size), dtype=bool)
y = np.zeros((len(sequences), vocab_size), dtype=bool)

# Fülle die Arrays
for i, sequence in enumerate(sequences):
    for t, char in enumerate(sequence):
        X[i, t, char_to_idx[char]] = 1  # Setze das entsprechende Bit auf 1
    y[i, char_to_idx[next_chars[i]]] = 1

print(f"X shape: {X.shape}")  # (Anzahl Beispiele, Sequenzlänge, Vokabular)
print(f"y shape: {y.shape}")  # (Anzahl Beispiele, Vokabular)
print("\nFertig! Daten sind vorbereitet.")
print("\nNächster Schritt: RNN-Modell bauen (kommt gleich...)")
