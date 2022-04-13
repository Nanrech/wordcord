from os import path
from json import load
from pathlib import Path
PATH = Path(path.dirname(path.realpath(__file__)))

with open(Path(PATH, "txt/token"), "r") as f:
    TOKEN = f.read()


with open(Path(PATH, "txt/wordles.txt")) as kk:
    w = kk.read()
    VALIDS = w.split("\n")


with open(Path(PATH, "txt/wordle-allowed-guesses.txt")) as kk:
    w = kk.read()
    WORDS = w.split("\n")


with open(Path(PATH, "config.json"), "r") as S:
    __LOADED: dict = load(S)
valid_chr: list = __LOADED["valids"]
SCOPES: list = __LOADED["scopes"]
GRAY_S: str = __LOADED["gray"]
today: int = __LOADED["today"]
