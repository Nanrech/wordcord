from json import dump as j_dump
from json import load as j_load
from pathlib import Path
from random import randint
from os import stat
from os import path
from os import remove
from os.path import exists

from wordcord.master.resources.consts import WORDS

__PATH = Path(path.dirname(path.realpath("./users")))
PATH = Path(path.dirname(path.realpath(__file__)))


def wnc(inp):
    if inp is None:
        return False
    for a in inp:
        if a == "🟩":
            continue
        else:
            return False
    return True


def err(inp, chars, valids):
    if not isinstance(inp, str):
        return "Invalid format. Guess must be a string."  # error
    for ch in inp:
        if ch not in chars:
            return "Invalid Character. Guesses must only contain characters from a to Z."  # error
        else:
            continue
    if len(inp) != 5:
        return "Invalid length. Guesses must be 5 letter long words."  # error
    if inp.lower() not in valids:
        return "Invalid Word. Couldn't find word in the valid words database."  # error
    return True  # , None


def gss(gues, wrdl):
    n = 0
    load = []
    for x in gues.lower():
        if x == wrdl[n]:
            load.append("🟩")
            n += 1
            continue
        elif x in wrdl and x != wrdl[n]:
            load.append("🟨")
            n += 1
            continue
        else:
            load.append("⬛")
            n += 1
            continue
    return "".join(load)


def prf_exists(user: str):
    pth = f"./users/{user}.json"
    if exists(pth) and stat(pth).st_size != 0:
        return True
    else:
        try:
            with open(pth, "x") as _:
                pass
        except FileExistsError:
            pass
        with open(pth, "w") as f:
            sample = {"tries": "", "guesses": "", "streak": 0}
            j_dump(sample, f)
        return False


def clear_prf(pid: str, hard: bool = False):
    prf_exists(pid)
    pth = f"./users/{pid}.json"
    with open(pth, "r") as g:
        yy = j_load(g)
    yy["guesses"] = ""
    yy["tries"] = ""
    if hard:
        yy["streak"] = 0
    with open(pth, "w") as g:
        j_dump(yy, g)
    return


def nuker(user: str):
    try:
        remove(f"{Path(__PATH, 'users')}\\{user}.json")
        return True
    except FileNotFoundError:
        return False


def post_toDB(pid: str, gs, wrdle: str):
    pth = f"./users/{pid}.json"
    prf_exists(pid)
    with open(pth, "r") as g:
        d = j_load(g)
    with open(pth, "w") as g:
        d["guesses"] = d["guesses"] + gs
        d["tries"] = d["tries"] + gss(gs, wrdl=wrdle)
        j_dump(d, g)


def streak_modify(pid: str, amount: int = 1):
    pth = f"./users/{pid}.json"
    prf_exists(pid)
    with open(pth, "r") as g:
        d = j_load(g)
    if d["streak"] < 0:
        d["streak"] = 0
    with open(pth, "w") as g:
        d["streak"] = d["streak"] + amount
        j_dump(d, g)


def fetch_profile(pid: str):
    pth = f"./users/{pid}.json"
    with open(pth, "r") as g:
        return dict(j_load(g))


def gen_wordle():
    word = WORDS[randint(0, len(WORDS))]

    with open(Path(PATH, "config.json"), "r") as S:
        _cfg: dict = j_load(S)

    with open(Path(PATH, "config.json"), "w") as S:
        _cfg["wordle"] = word
        j_dump(_cfg, S)


def get_wordle() -> str:
    with open(Path(PATH, "config.json"), "r") as S:
        return str(j_load(S)["wordle"])
