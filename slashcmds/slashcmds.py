import discord
from discord.ext import commands
from core.models import PermissionLevel
from dislash import InteractionClient, ActionRow, Button, ButtonStyle





class SlashCmds(commands.Cog):
    """
    Slash Commands (TESTING)
    """
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.client = Client()
        
        
def setup(bot):
    bot.add_cog(SlashCmds(bot))
