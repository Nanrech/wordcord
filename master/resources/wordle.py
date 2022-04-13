from pathlib import Path
from json import load, dump
from random import randint

from wordcord.master.resources.consts import PATH

with open(Path(PATH, "txt/wordles.txt")) as kk:
    w = kk.read()
    VALIDS = w.split("\n")

with open(Path(PATH, "txt/wordle-allowed-guesses.txt")) as kk:
    w = kk.read()
    WORDS = w.split("\n")

wordle = WORDS[randint(0, len(WORDS))]

with open(Path(PATH, "config.json"), "r") as S:
    _cfg: dict = load(S)

with open(Path(PATH, "config.json"), "w") as S:
    _cfg["wordle"] = wordle
    dump(_cfg, S)
