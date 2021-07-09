import discord,nekosbest,requests,json
from discord.ext import commands
from nekosbest import Client
from typing import Optional
from box import Box
from core import checks
from core.models import PermissionLevel

class Nekos(commands.Cog):
    """
    Nekos! Made by Abadima
    """
    def __init__(self, bot):
        self.bot = bot
        self.client = Client()

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def neko(self, ctx):
        """Neko Pictures!"""
        author = ctx.author
        result = await self.client.get_image("nekos")
        embed = discord.Embed(colour=author.colour)
        embed.title = f"Neko!~"
        embed.set_image(url=result.url)
        await ctx.reply(embed=embed)
        
    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def neko2(self, ctx):
        """Neko Pictures! Pt. 2"""
        author = ctx.author
        result = requests.get("https://nekos.life/api/v2/img/neko")
        result = result.json()
        boxed = Box(result)
        data = (boxed.data.children).data
        image = data.url
        embed = discord.Embed(colour=author.colour)
        embed.title = f"Neko!~"
        embed.set_image(url=image)
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Nekos(bot))
