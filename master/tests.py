import json, os
from typing import Union
from os.path import exists

wordle = 'craft'


def gss(gues):
    n = 0
    load = []
    for x in gues.lower():
        if x == wordle[n]:
            load.append('🟩')
            n += 1
            continue
        elif x in wordle and x != wordle[n]:
            load.append('🟨')
            n += 1
            continue
        else:
            load.append('⬛')
            n += 1
            continue
    return ''.join(load)


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
            sample = {"tries": "", "guesses": "", "streak": 0, "beaten": False}
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
        d["tries"] = d["tries"] + gss(gs)
        json.dump(d, g)


def fetch_profile(pid: str):
    pth = f"./users/{pid}.json"
    with open(pth, "r") as g:
        return dict(json.load(g))


"""
guess = "pears"
prf_exists("765765765761")
softclear_prf("765765765761")
post_tries("765765765761", gss(guess))
post_guess("765765765761", guess)
with open("./users/765765765761.json", "r", encoding="utf-8") as f:
    g: dict = json.load(f)
print(g["tries"][0:5])
print(len(g["tries"]), int(len(g["tries"]) / 5))
print(gss("cramp"))
"""