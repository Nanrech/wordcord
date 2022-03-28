from json import dump as j_dump
from json import load as j_load
from os import stat
from os.path import exists
from typing import Union
from wordcord.master.resources.wordle import wordle


def err(inp, chars, valids):
    if not isinstance(inp, str):
        return False
    tta: str = inp.lower()
    if len(tta) != 5:
        return False  # , error
    for ch in inp:
        if ch not in chars:
            return False  # , error
        else:
            continue
    if tta not in valids:
        return False
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
        return
    else:
        try:
            with open(pth, "x") as _:
                pass
        except FileExistsError:
            pass
        with open(pth, "w") as f:
            sample = {"tries": "", "guesses": "", "streak": 0}
            j_dump(sample, f)
        return


def softclear_prf(pid: str):
    pth = f"./users/{pid}.json"
    with open(pth, "r") as g:
        yy = j_load(g)
    yy["guesses"] = ""
    yy["tries"] = ""
    with open(pth, "w") as g:
        j_dump(yy, g)
    return


def post_toDB(pid: Union[str, int], gs):
    pth = f"./users/{pid}.json"
    prf_exists(pid)
    with open(pth, "r") as g:
        d = j_load(g)
    with open(pth, "w") as g:
        d["guesses"] = d["guesses"] + gs
        d["tries"] = d["tries"] + gss(gs, wrdl=wordle)
        j_dump(d, g)


def fetch_profile(pid: str):
    pth = f"./users/{pid}.json"
    with open(pth, "r") as g:
        return dict(j_load(g))


def wnc(inp):
    if inp is None:
        return False
    for a in inp:
        if a == "🟩":
            continue
        else:
            return False
    return True
