from random import randint
from pathlib import Path
from wordcord.master.resources.consts import PATH

with open(Path(PATH, "wordles.txt")) as kk:
    w = kk.read()
    VALIDS = w.split("\n")
with open(Path(PATH, "wordle-allowed-guesses.txt")) as kk:
    w = kk.read()
    WORDS = w.split("\n")
wordle = WORDS[randint(0, len(WORDS))]
