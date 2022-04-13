import time
import datetime

import interactions

from wordcord.master.resources.consts import SCOPES, GRAY_S
from wordcord.master.resources.funcs import clear_prf, nuker, prf_exists, fetch_profile, get_wordle, gen_wordle
from wordcord.master.resources.permissions import has_permission


class AdminCMD(interactions.Extension):

    def __init__(self, client: interactions.Client):
        self.bot: interactions.Client = client

    @interactions.extension_command(name="clear", description="🔐 Clears a player's profile, bot administrators only",
                                    scope=SCOPES,
                                    options=[
                                        interactions.Option(name="user", description="User",
                                                            type=interactions.OptionType.STRING, required=True)])
    async def _soft_clear(self, ctx: interactions.CommandContext, user: str):
        if not user.isnumeric():
            return await ctx.send("Invalid user ID. User IDs can only be numbers", ephemeral=True)
        if int(ctx.author.user.id) != 452954731162238987:  # Hardcoded to be Nan#5809's ID
            return await ctx.send("🔐 This command can only be ran by bot administrators.", ephemeral=True)
        clear_prf(user)
        return await ctx.send(f"`{user}.json` cleared")

    @interactions.extension_command(name="wipe", description="🔐 Wipes a player's profile, bot administrators only",
                                    scope=SCOPES,
                                    options=[
                                        interactions.Option(name="user", description="User",
                                                            type=interactions.OptionType.STRING, required=True)])
    async def _hard_clear(self, ctx: interactions.CommandContext, user: str):
        if not user.isnumeric():
            return await ctx.send("Invalid user ID. User IDs can only be numbers", ephemeral=True)
        if int(ctx.author.user.id) != 452954731162238987:  # Hardcoded to be Nan#5809's ID
            return await ctx.send("🔐 This command can only be ran by bot administrators.", ephemeral=True)
        clear_prf(user, hard=True)
        return await ctx.send(f"`{user}.json` wiped")

    @interactions.extension_command(name="nuke", description="🔐 Nukes a player's profile, bot administrator only",
                                    scope=SCOPES,
                                    options=[
                                        interactions.Option(name="user", description="User",
                                                            type=interactions.OptionType.STRING, required=True)])
    async def _nuker(self, ctx: interactions.CommandContext, user: str):
        if not user.isnumeric():
            return await ctx.send("Invalid user ID. User IDs can only be numbers", ephemeral=True)
        if int(ctx.author.user.id) != 452954731162238987:  # Hardcoded to be Nan#5809's ID
            return await ctx.send("🔐 This command can only be ran by bot administrators.", ephemeral=True)
        if not nuker(user):
            return await ctx.send(f"`{user}.json` doesn't exist", ephemeral=True)
        await ctx.send(f"`{user}.json` deleted", ephemeral=True)

    @interactions.extension_command(name="reveal",
                                    description="🔒 Reveals the currently active Wordle",
                                    scope=SCOPES)
    async def _emb(self, ctx: interactions.CommandContext):
        if not has_permission(ctx.author.permissions, 13):
            return await ctx.send(
                content="🔒 This command can only be ran by members with the `MANAGE_MESSAGES` permission.",
                ephemeral=True)
        await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                                 description=f"Today's current word is ||`{get_wordle()}`||!",
                                                 color=0x5865F2))

    @interactions.extension_command(name="re-roll",
                                    description="🔒 Re-rolls the currently active Wordle",
                                    scope=SCOPES)
    async def _swap(self, ctx: interactions.CommandContext):
        if int(ctx.author.user.id) != 452954731162238987:  # Hardcoded to be Nan#5809's ID
            return await ctx.send("🔐 This command can only be ran by bot administrators.", ephemeral=True)
        gen_wordle()
        await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                                 description=f"Changed current wordle to ||`{get_wordle()}`||!",
                                                 color=0x5865F2))

    @interactions.extension_command(name="ping",
                                    description="Shows the bot's ping",
                                    scope=SCOPES)
    async def _ping(self, ctx: interactions.CommandContext):
        await ctx.send(embeds=interactions.Embed(
            title=f"<t:{int(time.time())}>",
            description=f"{int(self.client.latency)} ms 🏓",
            color=0x5865F2))

    @interactions.extension_command(name="spy",
                                    description="🔒 Shows another user's current session",
                                    scope=SCOPES,
                                    options=[
                                        interactions.Option(
                                            name="user",
                                            description="Who to spy on",
                                            required=True,
                                            type=interactions.OptionType.USER),
                                        interactions.Option(
                                            name="show",
                                            description="Whether to show this to the public or not",
                                            required=False,
                                            type=interactions.OptionType.STRING,
                                            choices=[
                                                interactions.Choice(name="Show", value="ye"),
                                                interactions.Choice(name="Don't show",
                                                                    value="na")])])
    async def _spy(self, ctx: interactions.CommandContext, user: interactions.Member, show: str = "na"):
        if user.user.bot:
            return await ctx.send("We love bots but, sadly, they can't play Wordle. Try again with someone else.",
                                  ephemeral=True)
        U = str(user.id)
        prf_exists(U)
        tries = str(dict(fetch_profile(U))["tries"])
        if tries == "":
            return await ctx.send(content="No current session found", ephemeral=True)
        a = [tries[x:x + 5] for x in range(0, len(tries), 5)]
        if has_permission(ctx.author.permissions, 13):
            guesses = str(dict(fetch_profile(U))["guesses"]).upper()
            b = [guesses[x:x + 5] for x in range(0, len(guesses), 5)]
            fields = "\n".join(' '.join(x) for x in zip(a, b))
        else:
            fields = "\n".join(a)
        msg = interactions.Embed(
            title=f"{user.user.username}#{user.user.discriminator}'s session",
            footer=interactions.EmbedFooter(text=f"ID: {U}"),
            color=0x5865F2,
            fields=[interactions.EmbedField(name="🕵️", value=fields.replace("⬛", GRAY_S))])
        await ctx.send(embeds=msg, ephemeral=(show == "na"))


def setup(client: interactions.Client):
    AdminCMD(client)
