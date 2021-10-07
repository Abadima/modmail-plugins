import discord
from discord.ext import commands
from core.models import PermissionLevel
from core import checks
from dislash import InteractionClient, ActionRow, Button, ButtonStyle





class SlashCmds(commands.Cog):
    """
    Slash Commands (TESTING)
    """
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def test(self, ctx: commands.Context):
        """***NOT FUNCTIONAL***"""
        await ctx.reply('seriously, this feature is still W.I.P',components = [ActionRow(Button(style=ButtonStyle.link, label="The Useless Web", url="https://theuselessweb.com/"))])
        
        
def setup(bot):
    bot.add_cog(SlashCmds(bot))
