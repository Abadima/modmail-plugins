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
        embed.add_field(name="Duration", value=self.bot.uptime)
        embed.add_field(name="Heroku Boot:", value=_format_time(self._boot_time))
        embed.add_field(name="Bot Boot:", value=_format_time(self._bot_time))
        await ctx.reply(embed=embed)
        
    @commands.command(aliases=["mcount"])
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.REGULAR)
    @commands.cooldown(1, 2, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def membercount(self, ctx):
        """Member Counts"""
        cGuild = ctx.guild.member_count
        cHuman = [member for member in ctx.guild.members if not member.bot]
        cBot = [member for member in ctx.guild.members if member.bot]
        author = ctx.author
        embed = discord.Embed(colour=author.colour)
        embed.title = f"Member Count"
        embed.add_field(name="Members", value=cGuild)
        embed.add_field(name="Humans", value=cHuman)
        embed.add_field(name="Bots", value=cBot)
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))
