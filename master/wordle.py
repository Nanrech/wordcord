import random

with open('../resources/wordles.txt') as kk:  # Temp
    w = kk.read()
    WORDS = w.split("\n")
wordle = WORDS[random.randint(0, len(WORDS))]  # Temp
