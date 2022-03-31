import interactions

from wordcord.master.resources.consts import TOKEN, valid_chr, SCOPES, YELLOW_A, GREEN_A, today
from wordcord.master.resources.funcs import prf_exists, softclear_prf, post_toDB, fetch_profile, err, wnc, gss
from wordcord.master.resources.wordle import wordle, VALIDS

# Wordle!
bot = interactions.Client(token=TOKEN)


@bot.event
async def on_ready():
    print("Online!")


@bot.command(name="dbug", description="Sends a test command", scope=SCOPES)
async def _emb(ctx: interactions.CommandContext):
    await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                             description=f"Today's current word is ||`{wordle}`||!",
                                             color=0x6aaa64))


@bot.command(name="admin-clear", description="Removes a player's profile", scope=SCOPES, options=[
    interactions.Option(name="user", description="User", type=interactions.OptionType.USER, required=True)])
async def _soft_clear(ctx: interactions.CommandContext, user: interactions.Member):
    try:
        softclear_prf(str(user.id))
        return await ctx.send(f"Cleared user: {user.user.username}#{user.user.discriminator}")
    except FileNotFoundError:
        return await ctx.send(f"{user.user.username}#{user.user.discriminator} doesn't have a profile")


@bot.command(name="guess", description="Submit a wordle guess", scope=SCOPES, options=[interactions.Option(
    name="guess", description="A string containing your guess", type=interactions.OptionType.STRING, required=True)])
async def submit(ctx: interactions.CommandContext, guess):
    U = ctx.author.user.id
    if not err(inp=guess.lower(), chars=valid_chr, valids=VALIDS):
        return await ctx.send("Guess was incorrectly formatted")
    if int(len(dict(fetch_profile(U))["guesses"]) / 5) == 6:
        return await ctx.send("Max. number of tries reached")
    if wnc(dict(fetch_profile(U))["tries"][-5:]) and dict(fetch_profile(U))["tries"] != "":
        return await ctx.send("⭐ - You already won today, no need to guess again! - ⭐")
    prf_exists(U)
    post_toDB(pid=ctx.author.user.id, gs=guess)
    tries = str(dict(fetch_profile(U))["tries"])
    guesses = str(dict(fetch_profile(U))["guesses"]).upper()
    a = [tries[x:x + 5] for x in range(0, len(tries), 5)]
    b = [guesses[x:x + 5] for x in range(0, len(guesses), 5)]
    fields = "\n".join(' '.join(x) for x in zip(a, b))
    if wnc(gss(guess, wordle)):
        emji = GREEN_A
        clr = 0x6aaa64
        win_msg = f"Wordcord {today} \n"
    else:
        emji = YELLOW_A
        clr = 0xffde59
        win_msg = ""
    msg = interactions.Embed(
        title=f"{emji} Wordle",
        color=clr,
        fields=[interactions.EmbedField(name=f"Wordcord {today} {len(a)}/6\n", value=win_msg + fields)])
    # (name="Tries:\n", value="\n".join([tries[x:x+5] for x in range(0, len(tries), 5)]))]) for JUST the squares

    await ctx.send(embeds=msg, ephemeral=True)


@bot.command(name="current", description="Shows your current game's status. Can be public or private",
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
    if wnc(dict(fetch_profile(U))["tries"][-5:]):
        emji = "<:A_s:958125488642088980> "
        clr = 0x6aaa64
    else:
        emji = "<:A_p:958127218142347356> "
        clr = 0xffde59
    msg = interactions.Embed(
        title=f"{emji} Wordle",
        color=clr,
        fields=[interactions.EmbedField(name=f"Wordcord {today} {len(a)}/6\n", value=fields)])
    await ctx.send(embeds=msg, ephemeral=not (show == "ye"))


bot.start()
