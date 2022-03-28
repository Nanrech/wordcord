import json
import os
from os.path import exists
from typing import Union
from wordle import wordle


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
    if exists(pth) and os.stat(pth).st_size != 0:
        return
    else:
        try:
            with open(pth, "x") as _:
                pass
        except FileExistsError:
            pass
        with open(pth, "w") as f:
            sample = {"tries": "", "guesses": "", "streak": 0}
            json.dump(sample, f)
        return


def softclear_prf(pid: str):
    pth = f"./users/{pid}.json"
    with open(pth, "r") as g:
        yy = json.load(g)
    yy["guesses"] = ""
    yy["tries"] = ""
    with open(pth, "w") as g:
        json.dump(yy, g)
    return


def post_toDB(pid: Union[str, int], gs):
    pth = f"./users/{pid}.json"
    prf_exists(pid)
    with open(pth, "r") as g:
        d = json.load(g)
    with open(pth, "w") as g:
        d["guesses"] = d["guesses"] + gs
        d["tries"] = d["tries"] + gss(gs, wrdl=wordle)
        json.dump(d, g)


def fetch_profile(pid: str):
    pth = f"./users/{pid}.json"
    with open(pth, "r") as g:
        return dict(json.load(g))
