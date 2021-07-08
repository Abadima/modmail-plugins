import discord,nekosbest
from discord.ext import commands
from nekosbest import Client
from typing import Optional

class Nekos(commands.Cog):
    """
    Nekos! Made by Abadima
    """
    def __init__(self, bot):
        self.bot = bot
        self.client = Client()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def neko(self, ctx):
        """Neko Pictures!"""
        author = ctx.author
        result = await self.client.get_image("nekos")
        embed = discord.Embed(colour=author.colour)
        embed.description = f"Neko!"
        embed.set_image(url=result.url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Action(bot))
