import interactions
import os

from pathlib import Path
from os import path
from wordcord.master.resources.consts import TOKEN, valid_chr, SCOPES, GRAY_S, today
from wordcord.master.resources.funcs import prf_exists, post_toDB, fetch_profile, err, wnc
from wordcord.master.resources.wordle import wordle, VALIDS

# Wordle!
bot = interactions.Client(token=TOKEN)
_PATH = Path(path.dirname(path.realpath(__file__)))


@bot.event
async def on_ready():
    print("Online!")


@bot.command(name="try", description="Submit a guess for today's Wordle", scope=SCOPES, options=[interactions.Option(
    name="guess", description="A string containing your choice", type=interactions.OptionType.STRING, required=True)])
async def submit(ctx: interactions.CommandContext, guess):
    U = ctx.author.user.id
    if not err(inp=guess.lower(), chars=valid_chr, valids=VALIDS):
        return await ctx.send(ephemeral=True, embeds=interactions.Embed(
            title="Guess was incorrectly formatted",
            description="A guess can only be 5 letters long and must only contain characters from a to Z",
            color=0x5865F2
        ))
    if int(len(dict(fetch_profile(U))["guesses"]) / 5) == 6:
        return await ctx.send(ephemeral=True, embeds=interactions.Embed(
            title=f"Max. number of tries reached",
            color=0x5865F2,
            description="Run `/current` to see all your guesses"
        ))
    if wnc(dict(fetch_profile(U))["tries"][-5:]) and dict(fetch_profile(U))["tries"] != "":
        return await ctx.send(ephemeral=True,
                              embeds=interactions.Embed(
                                  title=f"You already beat today's Wordle! :star:",
                                  color=0x5865F2,
                                  description="If you want to, you can run `/current` \nto get your last recorded "
                                              "Wordcord session"
                              ))
    prf_exists(U)
    post_toDB(pid=ctx.author.user.id, gs=guess)
    tries = str(dict(fetch_profile(U))["tries"])
    guesses = str(dict(fetch_profile(U))["guesses"]).upper()
    a = [tries[x:x + 5] for x in range(0, len(tries), 5)]
    b = [guesses[x:x + 5] for x in range(0, len(guesses), 5)]
    fields = "\n".join(' '.join(x) for x in zip(a, b))
    clr = 0x6aaa64 if wnc(dict(fetch_profile(U))["tries"][-5:]) else 0xffde59
    final = "​" if len(a) != 6 else f"Oops! The correct answer was ||{wordle.upper()}||!"
    msg = interactions.Embed(
        title=f"Wordle {today} {len(b)}/6",
        color=clr,
        fields=[interactions.EmbedField(name=final, value=fields.replace("⬛", GRAY_S))])
    # The name parameter has a zero width character because I couldn't pass in an empty string
    # Shitty solution, but it looks alright. Same applies to /current
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
async def _status(ctx: interactions.CommandContext, show: str = None):
    U = ctx.author.id
    tries = str(dict(fetch_profile(U))["tries"])
    if tries == "":
        return await ctx.send(content="No current session found", ephemeral=True)
    guesses = str(dict(fetch_profile(U))["guesses"]).upper()
    U = ctx.author.user.id
    a = [tries[x:x + 5] for x in range(0, len(tries), 5)]
    b = [guesses[x:x + 5] for x in range(0, len(guesses), 5)]
    fields = "\n".join(' '.join(x) for x in zip(a, b))
    clr = 0x6aaa64 if wnc(dict(fetch_profile(U))["tries"][-5:]) else 0xffde59
    final = "​" if len(a) != 6 else f"Oops! The correct answer was ||{wordle.upper()}||!"
    msg = interactions.Embed(
        title=f"Wordle {today} {len(b)}/6",
        color=clr,
        fields=[interactions.EmbedField(name=final, value=fields.replace("⬛", GRAY_S))])
    await ctx.send(embeds=msg, ephemeral=not (show == "ye"))

cogs = [
    module[:-3]
    for module in os.listdir(f"{Path(_PATH, 'cogs')}")
    if module[-3:] == ".py"
]
for cog in cogs:
    bot.load("cogs." + cog)


bot.start()
