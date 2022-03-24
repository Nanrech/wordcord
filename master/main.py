import random, os, json
import interactions

# Wordle!
SCOPES = '749015533310967828'  # Temp
with open('../resources/token') as f:
    TOKEN = f.read()
bot = interactions.Client(token=TOKEN)
with open('../resources/types/wordles.txt') as kk:  # Temp
    w = kk.read()
    WORDS = w.split("\n")
valid_chr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z']  # Temp
wordle = WORDS[random.randint(0, len(WORDS))]  # Temp
player_current: list = []  # Temp
player_guesses: list = []  # Temp
today = '1'  # Temp


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


def profiler(us):
    dat: dict = {f'{us}': {
        "streak": 3,
        "mode": "Wordle",
        "beaten": False,
        "tries": [],
        "guesses": []
    }}
    return dat


'''
{
  "2": {
    "tries": [],
    "guesses": [],
    "streak": 5,
    "beaten": false
  }
}'''


def err(inp, chars, valids):
    if len(inp) != 5:
        return False  # , error
    for ch in inp:
        if ch not in chars:
            return False  # , error
        else:
            continue
    if inp not in valids:
        return False
    return True  # , None


def wnc(inp):
    for a in inp:
        if a == '🟩':
            continue
        else:
            return False
    return True


@bot.event
async def on_ready():
    print("Online!")


@bot.command(name='dbug', description='Sends a test command', scope=SCOPES)
async def emb(ctx: interactions.CommandContext):
    await ctx.send(str(ctx._json))
    await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                             description=f"Today's current word is ||`{wordle}`||!",
                                             color=0x56AB91))


@bot.command(name='guess', description='Submit a wordle guess', scope=SCOPES, options=[interactions.Option(
    name='guess', description='A string containing your guess', type=interactions.OptionType.STRING, required=True)])
async def submit(ctx: interactions.CommandContext, guess):
    if not err(inp=guess, chars=valid_chr, valids=WORDS):
        return await ctx.send("Guess was incorrectly formatted - PLACEHOLDER TEXT")
    prf_exists(str(ctx.author.user.id))
    with open(f"./users/{ctx.author.user.id}.json", "r") as l:
        profile = json.load(l)
    profile["tries"] = profile["tries"].append(gss(guess))
    profile["guesses"] = profile["guesses"].append(guess)


"""

ERR func -> Checks if stuff is cool or not, returns a true/false with the reason why it's not cool or None
if guess in WORDS ->
check if beaten:
WNC func -> returns true if all the squares in a tryfied are green

    if len(player_current) != 0:
        if wnc(player_current[-1]):
            return await ctx.send('You already won, no need to try again.', ephemeral=True)
    
    if len(player_current) >= 6:
        return await ctx.send(f'Max. number of tries reached. The word was ||{wordle}||', ephemeral=True)

"""
