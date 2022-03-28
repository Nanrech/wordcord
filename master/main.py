from wordcord.master.resources.wordle import wordle, VALIDS
from wordcord.master.resources.consts import TOKEN, valid_chr, SCOPES, YELLOW_A, GREEN_A
import interactions
from interactions import Client, CommandContext, Option, OptionType, Choice, Member
from wordcord.master.resources.funcs import prf_exists, softclear_prf, post_toDB, fetch_profile, err, wnc

# Wordle!
bot = Client(token=TOKEN)


@bot.event
async def on_ready():
    print("Online!")


@bot.command(name="dbug", description="Sends a test command", scope=SCOPES)
async def _emb(ctx: CommandContext):
    await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                             description=f"Today's current word is ||`{wordle}`||!",
                                             color=0x6aaa64))


@bot.command(name="admin-clear", description="Removes a player's profile", scope=SCOPES, options=[
    Option(name="user", description="User", type=OptionType.USER, required=True)])
async def _soft_clear(ctx: CommandContext, user: Member):
    try:
        softclear_prf(str(user.id))
        return await ctx.send(f"Cleared user: {user.user.username}#{user.user.discriminator}")
    except FileNotFoundError:
        return await ctx.send(f"{user.user.username}#{user.user.discriminator} doesn't have a profile")


@bot.command(name="guess", description="Submit a wordle guess", scope=SCOPES, options=[Option(
    name="guess", description="A string containing your guess", type=OptionType.STRING, required=True)])
async def submit(ctx: CommandContext, guess):
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
    if wnc(dict(fetch_profile(U))["tries"][-5:]):
        emji = GREEN_A
        clr = 0x6aaa64
    else:
        emji = YELLOW_A
        clr = 0xffde59
    msg = interactions.Embed(
        title=f"{emji} Wordle",
        color=clr,
        fields=[interactions.EmbedField(name="Attempts:", value=fields)])
    # (name="Tries:\n", value="\n".join([tries[x:x+5] for x in range(0, len(tries), 5)]))]) for JUST the squares

    await ctx.send(embeds=msg, ephemeral=True)


@bot.command(name="current", description="Shows your current game's status. Can be public or private",
             scope=SCOPES,
             options=[Option(name="show",
                             description="Whether to show this to the public or not",
                             required=False,
                             type=OptionType.STRING,
                             choices=[
                                 Choice(name="Show", value="ye"),
                                 Choice(name="Don't show", value="na")])])
async def _status(ctx: CommandContext, show: str = None):
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
        fields=[interactions.EmbedField(name="Attempts:", value=fields)])
    if show == "ye":
        await ctx.send(embeds=msg, ephemeral=False)
    else:
        await ctx.send(embeds=msg, ephemeral=True)


bot.start()
