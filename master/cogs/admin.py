import interactions

from wordcord.master.resources.consts import SCOPES
from wordcord.master.resources.wordle import wordle
from wordcord.master.resources.funcs import softclear_prf
from wordcord.master.resources.permissions import has_permission


class AdminCMD(interactions.Extension):

    def __init__(self, client: interactions.Client):
        self.bot: interactions.Client = client

    @interactions.extension_command(name="wipe", description="🔐 Wipes a player's profile, bot administrator only",
                                    scope=SCOPES,
                                    options=[
                                        interactions.Option(name="user", description="User",
                                                            type=interactions.OptionType.USER, required=True)])
    async def _soft_clear(self, ctx: interactions.CommandContext, user: interactions.Member):
        if int(ctx.author.user.id) != 452954731162238987:  # Hardcoded to be Nan#5809's ID
            return await ctx.send("🔐 This command can only be ran by designated bot administrators.", ephemeral=True)
        try:
            softclear_prf(str(user.id))
            return await ctx.send(f"Cleared user: {user.user.username}#{user.user.discriminator}")
        except FileNotFoundError:
            return await ctx.send(f"{user.user.username}#{user.user.discriminator} doesn't have a profile")

    @interactions.extension_command(name="reveal",
                                    description="🔒 Reveals the currently active Wordle",
                                    scope=SCOPES)
    async def _emb(self, ctx: interactions.CommandContext):
        if not has_permission(ctx.author.permissions, 13):
            return await ctx.send(
                content="🔒 This command can only be ran by members with the `MANAGE_MESSAGES` permission.",
                ephemeral=True)
        await ctx.send(embeds=interactions.Embed(title="**Wordle!**",
                                                 description=f"Today's current word is ||`{wordle}`||!",
                                                 color=0x5865F2))


def setup(client: interactions.Client):
    AdminCMD(client)
