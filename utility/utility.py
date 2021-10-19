import discord,requests,time,psutil
from discord.ext import commands
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
        humans = self.get_humans(ctx)
        bots = self.get_bots(ctx)
        embed = discord.Embed(colour=ctx.author.colour)
        embed.title = f"Member Count"
        embed.add_field(name="Members", value=ctx.guild.member_count)
        embed.add_field(name="Humans", value=humans)
        embed.add_field(name="Bots", value=bots)
        await ctx.reply(embed=embed)
        
    def get_bots(self, ctx):
        bots = [member for member in ctx.guild.members if member.bot]
        return len(bots)

    def get_humans(self, ctx):
        humans = [member for member in ctx.guild.members if not member.bot]
        return len(humans)

def setup(bot):
    bot.add_cog(Utilities(bot))
