import random
import interactions
import json

# Wordle!
SCOPES = '749015533310967828'
with open('../resources/token') as f:
    TOKEN = f.read()
bot = interactions.Client(token=TOKEN)
WORDS = []
for i in open('../resources/types/wordles.txt'):
    WORDS.append(i.replace('\n', ''))
valid_chr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z']
wordle = WORDS[random.randint(0, len(WORDS))]
player_current: list = []
player_guesses: list = []
today = '1'


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


def aeq(inp):
    it = 0
    for a in inp:
        if a == wordle[it]:
            it += 1
            continue
        else:
            return False
    return True


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
    "mode": "Wordle",
    "tries": [],
    "guesses": [],
    "streak": 5,
    "beaten": false
  }
}'''


def err(inp):
    if len(inp) != 5:
        return False
    for ch in inp:
        if ch not in valid_chr:
            return False
        else:
            continue
    return True


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


@bot.command(name='dump', description='dumps', scope=SCOPES, options=[interactions.Option(
    name='user', description='User you want to dump', type=interactions.OptionType.STRING, required=True)])
async def dump(ctx: interactions.CommandContext, user):
    with open('../resources/users.json', 'r') as d:
        data = json.load(d)
    await ctx.send(str(dict(data[user])))


@bot.command(name='test', description='Sends a test command', scope=SCOPES)
async def emb(ctx: interactions.CommandContext):
    await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                             description=f"Today's current word is ||`{wordle}`||!",
                                             color=0x56AB91))


@bot.command(name='start', description='Creates a user profile so your progress and stats can be saved. It is '
                                       'required to play the game!', scope=SCOPES)
async def start(ctx: interactions.CommandContext):
    with open('../resources/users.json', 'r+') as m:
        data = json.load(m)
        if str(ctx.author.user.id) in data:
            return await ctx.send('User profile already exists!')
    data.update(profiler(ctx.author.user.id))
    with open('../resources/users.json', 'w') as fm:
        json.dump(data, fm)
    await ctx.send('w')


@bot.command(name='submit', description='Submit a wordle guess', scope=SCOPES, options=[interactions.Option(
    name='guess', description='A string containing your guess', type=interactions.OptionType.STRING, required=True)])
async def submit(ctx: interactions.CommandContext, guess):
    with open('../resources/users.json') as k:
        if ctx.author.user.id not in k:
            await ctx.send('Run /start ')
    if not err(guess):
        return await ctx.send('Invalid input. Guesses must be 5 letter long words containing characters only from a '
                              'to z.')
    if len(player_current) != 0:
        if wnc(player_current[-1]):
            return await ctx.send('You already won, no need to try again.', ephemeral=True)
    if guess not in WORDS:
        return await ctx.send('Word not in word list.')
    if len(player_current) >= 6:
        return await ctx.send(f'Max. number of tries reached. The word was ||{wordle}||', ephemeral=True)
    player_current.append(gss(guess))
    player_guesses.append(guess)
    plygs = []
    it = 0
    for el in player_guesses:
        plygs.append(f'{player_current[it]}  -->  {el}')
        it += 1
    if wnc(gss(guess)):
        return await ctx.send(f"Wordle #{today} - {len(player_current)}/6\n\n" + '\n'.join(player_current))
    return await ctx.send(f"Wordle #{today} - {len(player_current)}/6\n\n" + '\n'.join(plygs), ephemeral=True)


bot.start()
