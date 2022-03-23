import json, os

wordle = 'craft'


def gss(guess):
    n = 0
    load = []
    for x in guess.lower():
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
    try:
        with open(f"./users/{user}.json", "x") as yu:
            with open(f"./users/{user}.json", "r") as uy:
                try:
                    yy = json.load(uy)
                except:
                    yy: dict = {}
            yy["tries"] = []
            yy["guesses"] = []
            yy["streak"] = 0
            yy["beaten"] = False
            with open(f"./users/{user}.json", "w") as uu:
                print(json.load(uu), yy)
                json.dump(yy, uu)

    except FileExistsError:
        return


def clear_prf(pid: str):
    with open(f"./users/{pid}.json", "r") as g:
        yy = json.load(g)
    yy["guesses"] = ""
    yy["tries"] = ""
    with open(f"./users/{pid}.json", "w") as g:
        json.dump(yy, g)
    return


def post_tries(pid: str, tri: str):
    with open(f"./users/{pid}.json", "r") as g:
        d = json.load(g)
    with open(f"./users/{pid}.json", "w") as g:
        d["tries"] = d["tries"] + tri
        json.dump(d, g)
    return


def post_guess(pid: str, gus: str):
    with open(f"./users/{pid}.json", "r") as g:
        d = json.load(g)
    with open(f"./users/{pid}.json", "w") as g:
        d["guesses"] = d["guesses"] + gus
        json.dump(d, g)
    return


def get_tries(pid: str):
    with open(f"./users/{pid}.json", "r") as g:
        return str(dict(json.load(g))["tries"])


guess = "craft"
#clear_prf('76576576576')
post_tries("76576576576", gss(guess))
post_guess("76576576576", guess)
