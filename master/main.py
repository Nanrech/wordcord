import random
import interactions
from tests import prf_exists, softclear_prf, post_toDB, gss, fetch_profile

# Wordle!
SCOPES = ['749015533310967828']  # Temp
with open('../resources/token') as f:
    TOKEN = f.read()
bot = interactions.Client(token=TOKEN)
with open('../resources/wordles.txt') as kk:  # Temp
    w = kk.read()
    WORDS = w.split("\n")
valid_chr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z']  # Temp
wordle = WORDS[random.randint(0, len(WORDS))]  # Temp
player_current: list = []  # Temp
player_guesses: list = []  # Temp
today = '1'  # Temp
SCOPES = "749015533310967828"


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
    await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                             description=f"Today's current word is ||`{wordle}`||!",
                                             color=0x56AB91))


@bot.command(name='admin-clear', description='Removes a player\'s profile', scope=SCOPES, options=[
    interactions.Option(name="user", description="User", type=interactions.OptionType.USER, required=True)])
async def _soft_clear(ctx: interactions.CommandContext, user):
    softclear_prf(user)
    F = await bot.http.get_user(user_id=user)
    await ctx.send(f"Cleared user: {dict(F)['username']}#{dict(F)['discriminator']}")


@bot.command(name='guess', description='Submit a wordle guess', scope=SCOPES, options=[interactions.Option(
    name='guess', description='A string containing your guess', type=interactions.OptionType.STRING, required=True)])
async def submit(ctx: interactions.CommandContext, guess):
    U = ctx.author.user.id
    if not err(inp=guess, chars=valid_chr, valids=WORDS):
        return await ctx.send("Guess was incorrectly formatted")
    if int(len(dict(fetch_profile(U))["tries"]) / 5) == 6:
        return await ctx.send("Max. number of tries reached")
    prf_exists(str(U))
    post_toDB(pid=ctx.author.user.id, gs=guess)


bot.start()
