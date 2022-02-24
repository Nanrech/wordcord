import random
import interactions
import asyncio
from interactions import Client, Message
from interactions.ext.wait_for import wait_for, setup
import asyncio

"""import sqlite3

# DB stuff!
conn = sqlite3.connect('../resources/userbase.db')
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(unix)')"""

# Wordle!
SCOPES = '749015533310967828'  # Temp
with open('../resources/token') as f:
    TOKEN = f.read()
bot = interactions.Client(token=TOKEN)
setup(bot, add_method=True)
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
    "mode": "Wordle",
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


@bot.command(name='help', description='release me from this hell', scope=SCOPES, options=[interactions.Option(
    name='user', description='User you want to dump', type=interactions.OptionType.STRING, required=True)])
async def dump(ctx: interactions.CommandContext, user):
    await ctx.send(f'... {user}')


@bot.command(name='test', description='Sends a test command', scope=SCOPES)
async def emb(ctx: interactions.CommandContext):
    await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                             description=f"Today's current word is ||`{wordle}`||!",
                                             color=0x56AB91))


@bot.command(name='start', description='Creates a user profile so your progress and stats can be saved. It is '
                                       'required to play the game!', scope=SCOPES)
async def start(ctx: interactions.CommandContext):
    return await ctx.send(embeds=interactions.Embed(title='*Wordcord!*',
                                                    description=f'This currently does nothing but I like embeds @Nan <@{ctx.author.user.id}>',
                                                    
                                                    color=0x56AB91))


@bot.command(name='submit', description='Submit a wordle guess', scope=SCOPES, options=[interactions.Option(
    name='guess', description='A string containing your guess', type=interactions.OptionType.STRING, required=True)])
async def submit(ctx: interactions.CommandContext, guess):
    async with open('../resources/users.json', 'r+') as ñ:
        print(ñ[""])


buttons = [
    interactions.Button(style=interactions.ButtonStyle.SECONDARY, custom_id="left", label="◀"),
    interactions.Button(style=interactions.ButtonStyle.DANGER, custom_id="stop", label="🛑"),
    interactions.Button(style=interactions.ButtonStyle.SECONDARY, custom_id="right", label="▶")
]
action_row = interactions.ActionRow(components=buttons)
mario = interactions.Button(style=interactions.ButtonStyle.DANGER, custom_id="mar", label="pls")
embedl = [interactions.Embed(title='*1! Haha!',
                             description='This is the 1st page.. woo',
                             color=0x75CB18),
          interactions.Embed(title='***2***',
                             description='Second page, almost there!',
                             color=0x65AB19),
          interactions.Embed(title='The final page!',
                             description='I wonder what the description for this one will look like',
                             color=0x75CB18)]


@bot.command(
    name="awe",
    description="this is just a test command.",
    scope=SCOPES
)
async def ayep(ctx):
    await ctx.send(embeds=embedl[0], components=action_row)


@bot.component('left')
async def left_bpress(ctx: interactions.ComponentContext):
    await ctx.edit(embeds=embedl[1])


@bot.component('right')
async def right_bpress(ctx: interactions.ComponentContext):
    await ctx.edit(embeds=embedl[1])


@bot.command(
    name="ayale", description="this is just a test command.", scope=SCOPES
)
async def aya(ctx: interactions.CommandContext):
    await ctx.send("grabbing a message...")

    async def check(msg):
        if int(msg.author.id) == int(ctx.author.user.id):
            return True
        await ctx.send("I wasn't asking you")
        return False

    try:
        msg: Message = await wait_for(
            bot, "on_message_create", check=check, timeout=15
        )
    except asyncio.TimeoutError:
        return await ctx.send("You said nothing :(")


bot.start()

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
