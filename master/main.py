import os
import datetime
import interactions
from os import path
from pathlib import Path

from wordcord.master.resources.consts import TOKEN, valid_chr, SCOPES, GRAY_S, today
from wordcord.master.resources.consts import VALIDS
from wordcord.master.resources.funcs import prf_exists, post_toDB, fetch_profile, err, wnc, get_wordle, gen_wordle, gss, streak_modify

# Wordle!
bot = interactions.Client(token=TOKEN, disable_sync=True)
_PATH = Path(path.dirname(path.realpath(__file__)))


@bot.event
async def on_ready():
    gen_wordle()
    print(f"Online! \n-scopes: {SCOPES}\n-cogs: {cogs}")


@bot.command(name="try", description="Submit a guess for today's Wordle", scope=SCOPES, options=[interactions.Option(
    name="guess", description="A string containing your choice", type=interactions.OptionType.STRING, required=True)])
async def submit(ctx: interactions.CommandContext, guess):
    if datetime.datetime.fromtimestamp(interactions.Snowflake(ctx.author.id).epoch) > datetime.datetime.now() - datetime.timedelta(days=7):
        return await ctx.send(ephemeral=True, embeds=interactions.Embed(
            title="Account must be at least a week old",
            description="To prevent spam, you won't be able to play until your account is at least 7 days old",
            color=0x5865F2
        ))
    if isinstance(err(inp=guess.lower(), chars=valid_chr, valids=VALIDS), str):
        return await ctx.send(ephemeral=True, embeds=interactions.Embed(
            title="Try again!",
            description=err(inp=guess.lower(), chars=valid_chr, valids=VALIDS),
            color=0x5865F2
        ))
    U = ctx.author.user.id
    prf_exists(U)
    profile = dict(fetch_profile(U))
    if int(len(profile["guesses"]) / 5) == 6:
        return await ctx.send(ephemeral=True, embeds=interactions.Embed(
            title=f"Max. number of tries reached",
            color=0x5865F2,
            description="Run `/current` to see all your guesses"
        ))
    if wnc(profile["tries"][-5:]) and profile["tries"] != "":
        return await ctx.send(ephemeral=True,
                              embeds=interactions.Embed(
                                  title=f"You already beat today's Wordle! :star:",
                                  color=0x5865F2,
                                  description="If you want to, you can run `/current` \nto get your last recorded "
                                              "Wordcord session"
                              ))
    wordle: str = get_wordle()
    prf_exists(U)
    if wnc(gss(guess, get_wordle())):
        streak_modify(U)
    post_toDB(pid=ctx.author.user.id, gs=guess, wrdle=wordle)
    profile: dict = fetch_profile(U)
    tries = str(profile["tries"])
    guesses = str(profile["guesses"]).upper()
    a = [tries[x:x + 5] for x in range(0, len(tries), 5)]
    b = [guesses[x:x + 5] for x in range(0, len(guesses), 5)]
    fields = "\n".join(' '.join(x) for x in zip(a, b))
    final = f"Streak: {profile['streak']}" if len(a) != 6 else f"Oops! The correct answer was ||{wordle.upper()}||!"
    msg = interactions.Embed(
        title=f"Wordle {today} {len(b)}/6",
        color=0x6aaa64 if wnc(profile["tries"][-5:]) else 0xffde59,
        fields=[interactions.EmbedField(name=final, value=fields.replace("⬛", GRAY_S))])
    # (name="Tries:\n", value="\n".join([tries[x:x+5] for x in range(0, len(tries), 5)]))]) for JUST the squares
    await ctx.send(embeds=msg, ephemeral=True)


@bot.command(name="current", description="Shows your current status. You can choose whether it's public or private",
             scope=SCOPES,
             options=[interactions.Option(name="show",
                                          description="Whether to show this to the public or not",
                                          required=False,
                                          type=interactions.OptionType.STRING,
                                          choices=[
                                              interactions.Choice(name="Show", value="ye"),
                                              interactions.Choice(name="Don't show", value="na")])])
async def _status(ctx: interactions.CommandContext, show: str = "na"):
    U = ctx.author.id
    prf_exists(U)
    profile = dict(fetch_profile(U))
    tries = str(profile["tries"])
    if tries == "":
        return await ctx.send(content="No current session found", ephemeral=True)
    wordle = get_wordle()
    guesses = str(profile["guesses"]).upper()
    a = [tries[x:x + 5] for x in range(0, len(tries), 5)]
    b = [guesses[x:x + 5] for x in range(0, len(guesses), 5)]
    fields = "\n".join(' '.join(x) for x in zip(a, b))
    clr = 0x6aaa64 if wnc(profile["tries"][-5:]) else 0xffde59
    final = f"Streak: {profile['streak']}" if len(a) != 6 else f"Oops! The correct answer was ||{wordle.upper()}||!"
    msg = interactions.Embed(
        title=f"Wordle {today} {len(b)}/6",
        color=clr,
        fields=[interactions.EmbedField(name=final, value=fields.replace("⬛", GRAY_S))])
    await ctx.send(embeds=msg, ephemeral=(show == "na"))


cogs = [
    module[:-3]
    for module in os.listdir(f"{Path(_PATH, 'cogs')}")
    if module[-3:] == ".py"
]
for cog in cogs:
    bot.load("cogs." + cog)


bot.start()
