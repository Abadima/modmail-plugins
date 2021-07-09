import discord,requests,time,psutil
from discord.ext import commands
from nekosbest import Client
from core import checks
from core.models import PermissionLevel

def _format_time(seconds):
    return time.ctime(seconds)

class Utilities(commands.Cog):
    """
    Utilities by Abadima
    """
    def __init__(self, bot):
        self.bot = bot
        self._load_time = time.time()
        self._boot_time = psutil.boot_time()
        self._bot_time = 0
        
    @commands.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @commands.cooldown(1, 2, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def uptime(self, ctx):
        """Uptime Statistics"""
    #    bot: discord.ext.commands.Bot = self.bot
        author = ctx.author
        embed = discord.Embed(colour=author.colour)
        embed.title = f"Uptime Statistics"
        embed.add_field(name="Uptime Duration", value=bot.uptime)
        embed.add_field(name="Cogs load time:", value=_format_time(self._load_time))
        embed.add_field(name="System boot time:", value=_format_time(self._boot_time))
        embed.add_field(name="Bot boot time:", value=_format_time(self._bot_time))
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))
