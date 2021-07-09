import discord,requests
from discord.ext import commands
from nekosbest import Client
from core import checks
from core.models import PermissionLevel

class Utilities(commands.Cog):
    """
    Utilities by Abadima
    """
    def __init__(self, bot):
        self.bot = bot
        self.client = Client()
        
    @commands.group(name="Utilities", aliases=["util"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def Utilities(self, ctx):
        """Neko's Utilities"""

        await ctx.send_help(ctx.command)
        
    @Utilities.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @commands.cooldown(1, 2, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def uptime(self, ctx):
        """Uptime Statistics"""
        bot: discord.ext.commands.Bot = self.bot
        author = ctx.author
        embed = discord.Embed(colour=author.colour)
        embed.title = f"Uptime Statistics"
        embed.add_field(name="Uptime", value=bot.uptime)
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))
