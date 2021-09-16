import sys,os,discord,logging
from discord.ext import commands
from core import checks
from core.models import PermissionLevel

logger = logging.getLogger('Modmail')


class Reboot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=["bathroom"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def reboot(self, ctx):
        """Clears Cached Logs & Reboots The Bot"""
        msg = await ctx.send(embed=discord.Embed(
            color=discord.Color.blurple(),
            description="Processing..."
        ))
        await ctx.invoke(self.bot.get_command('debug clear'))
        emsg = await msg.edit(embed=discord.Embed(
            color=discord.Color.blurple(),
            description="✅ Cleared Cached Logs"
        ))
        logger.info("==== Rebooting Bot ====")
        await msg.edit(embed=discord.Embed(
            color=discord.Color.blurple(),
            description="✅ | Rebooting...."
        ))
        os.execl(sys.executable, sys.executable, * sys.argv)


def setup(bot):
    bot.add_cog(Reboot(bot))
