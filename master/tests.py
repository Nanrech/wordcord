import json, os
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
    if exists(f"./users/{user}.json") and os.stat(f"./users/{user}.json").st_size != 0:
        return
    else:
        try:
            with open(f"./users/{user}.json", "x") as _:
                pass
        except FileExistsError:
            pass
        with open(f"./users/{user}.json", "w") as f:
            sample = {"tries": "", "guesses": "", "streak": 0, "beaten": False}
            json.dump(sample, f)
        return


def softclear_prf(pid: str):
    with open(f"./users/{pid}.json", "r") as g:
        yy = json.load(g)
    yy["guesses"] = ""
    yy["tries"] = ""
    with open(f"./users/{pid}.json", "w") as g:
        json.dump(yy, g)
    return


def post_tries(pid: str, tri: str):
    prf_exists(pid)
    with open(f"./users/{pid}.json", "r") as g:
        d = json.load(g)
    with open(f"./users/{pid}.json", "w") as g:
        d["tries"] = d["tries"] + gss(tri)
        json.dump(d, g)
    return


def post_guess(pid: str, gus: str):
    prf_exists(pid)
    with open(f"./users/{pid}.json", "r") as g:
        d = json.load(g)
    with open(f"./users/{pid}.json", "w") as g:
        d["guesses"] = d["guesses"] + gus
        json.dump(d, g)
    return


def get_tries(pid: str):
    with open(f"./users/{pid}.json", "r") as g:
        return str(dict(json.load(g))["tries"])


guess = "cramp"
#post_tries("765765765761", guess)
#post_guess("765765765761", guess)
with open(f"./users/765765765761.json", "r") as g:
    d = json.load(g)

c = 2
for a in d["tries"]:
    print(d["tries"][c])
    c += 1
    if c == 8:
        break
