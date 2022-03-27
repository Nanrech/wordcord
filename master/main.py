from wordle import wordle, WORDS
import interactions
from tests import prf_exists, softclear_prf, post_toDB, fetch_profile, gss

# Wordle!
with open('../resources/token') as f:
    TOKEN = f.read()
bot = interactions.Client(token=TOKEN)
valid_chr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z']  # Temp
player_current: list = []  # Temp
player_guesses: list = []  # Temp
today = '1'  # Temp
SCOPES = [749015533310967828]


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
    if inp is None:
        return False
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
async def _emb(ctx: interactions.CommandContext):
    await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                             description=f"Today's current word is ||`{wordle}`||!",
                                             color=0x56AB91))


@bot.command(name='admin-clear', description='Removes a player\'s profile', scope=SCOPES, options=[
    interactions.Option(name="user", description="User", type=interactions.OptionType.USER, required=True)])
async def _soft_clear(ctx: interactions.CommandContext, user: interactions.Member):
    try:
        softclear_prf(str(user.id))
        return await ctx.send(f"Cleared user: {user.user.username}#{user.user.discriminator}")
    except FileNotFoundError:
        return await ctx.send(f"{user.user.username}#{user.user.discriminator} doesn't have a profile")


@bot.command(name='guess', description='Submit a wordle guess', scope=SCOPES, options=[interactions.Option(
    name='guess', description='A string containing your guess', type=interactions.OptionType.STRING, required=True)])
async def submit(ctx: interactions.CommandContext, guess):
    U = ctx.author.user.id
    if not err(inp=guess, chars=valid_chr, valids=WORDS):
        return await ctx.send("Guess was incorrectly formatted")
    if int(len(dict(fetch_profile(U))["guesses"]) / 5) == 6:
        return await ctx.send("Max. number of tries reached")
    if wnc(dict(fetch_profile(U))["tries"][-5:]) and dict(fetch_profile(U))["tries"] != "":
        return await ctx.send("⭐ - You already won today, no need to guess again! - ⭐")
    prf_exists(U)
    post_toDB(pid=ctx.author.user.id, gs=guess)
    total = int(len(dict(fetch_profile(U))["guesses"]) / 5)
    tries = str(dict(fetch_profile(U))["tries"])
    msg = interactions.Embed(
        title="Wordle",
        color=0x6aaa64,
        fields=[interactions.EmbedField(name="Tries", value='\n'.join([tries[x:x+5] for x in range(0, len(tries), 5)]))])

    await ctx.send(embeds=msg)


bot.start()
