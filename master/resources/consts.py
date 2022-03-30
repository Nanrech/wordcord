from os import path
from pathlib import Path

PATH = Path(path.dirname(path.realpath(__file__)))
with open(Path(PATH, "text/token")) as f:
    TOKEN = f.read()
today = 0
SCOPES = [749015533310967828]
GREEN_A = "<:A_s:958125488642088980> "
YELLOW_A = "<:A_p:958127218142347356> "
valid_chr = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
             "v", "w", "x", "y", "z"]
