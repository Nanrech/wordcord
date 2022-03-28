import random

with open("../resources/wordle-allowed-guesses.txt") as kk:  # Temp
    w = kk.read()
    WORDS = w.split("\n")
with open("../resources/wordles.txt") as kk:
    w = kk.read()
    VALIDS = w.split("\n")
wordle = WORDS[random.randint(0, len(WORDS))]  # Temp
