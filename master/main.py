import random
import pprint
import interactions
import pymongo
from pymongo import MongoClient

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
cluster = MongoClient('mongodb+srv://NeverOne:A6XwrU17hfsHKHbR@cluster0.ivnqs.mongodb.net/test')
db = cluster['users_total']
collection = db['users_total']
posts = db.posts


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
async def dump(ctx: interactions.CommandContext):
    await ctx.send('...')


@bot.command(name='test', description='Sends a test command', scope=SCOPES)
async def emb(ctx: interactions.CommandContext):
    await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                             description=f"Today's current word is ||`{wordle}`||!",
                                             color=0x56AB91))


@bot.command(name='start', description='Creates a user profile so your progress and stats can be saved. It is '
                                       'required to play the game!', scope=SCOPES)
async def start(ctx: interactions.CommandContext):
    if collection.find_one({"_id": int(ctx.author.user.id)}) is not None:
        post = {"_id": int(ctx.author.user.id), "streak": 0, "mode": "Wordle", "beaten": False, "tries": [],
                "guesses": []}
        collection.insert_one(post)
        await ctx.send(embeds=interactions.Embed(title='*Wordcord!*',
                                                 description='Profile created in database',
                                                 color=0x56AB91))
    else:
        return await ctx.send(embeds=interactions.Embed(title='*Wordcord!*',
                                                        description='Profile already exists in database',
                                                        color=0x56AB91))


@bot.command(name='submit', description='Submit a wordle guess', scope=SCOPES, options=[interactions.Option(
    name='guess', description='A string containing your guess', type=interactions.OptionType.STRING, required=True)])
async def submit(ctx: interactions.CommandContext, guess):
    if not err(guess):
        return await ctx.send('Invalid input. Guesses must be 5 letter long words containing characters only from a to z.')
    if guess not in WORDS:
        return await ctx.send('Word not in word list.')
    if collection.find_one({"_id": int(ctx.author.user.id)}) is None:
        return await ctx.send('Run /start so you can play!')
    user = collection.find_one({"_id": int(ctx.author.user.id)})
    if len(list(user["guesses"])) >= 6:
        return await ctx.send('You already tried 6 times today!')
    if bool(user["beaten"]):
        return await ctx.send('You already beat the game today!')
    if wnc(gss(guess)):
        return collection.update_one({"_id": ctx.author.user.id},
                                     {"$set": {"guesses": list(user["guesses"]).append(guess),
                                               "tries": list(user["tries"]).append(gss(guess)),
                                               "beaten": True}})

    collection.update_one({"_id": ctx.author.user.id},
                          {"$set": {"guesses": list(user["guesses"]).append(guess),
                                    "tries": list(user["tries"]).append(gss(guess))}})


bot.start()

"""
    if len(player_current) != 0:
        if wnc(player_current[-1]):
            return await ctx.send('You already won, no need to try again.', ephemeral=True)
    
    if len(player_current) >= 6:
        return await ctx.send(f'Max. number of tries reached. The word was ||{wordle}||', ephemeral=True)
    
    
    
"""
