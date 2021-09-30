import discord,nekosbest,requests,json,asyncio
from discord.ext import commands
from nekosbest import Client
from core import checks
from core.models import PermissionLevel
from dislash.interactions import ActionRow, Button, ButtonStyle

class Nekos(commands.Cog):
    """
    Nekos! Made by Abadima
    """
    def __init__(self, bot):
        self.bot = bot
        self.client = Client()

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def neko(self, ctx):
        """Neko Pictures!"""
        author = ctx.author
        result = await self.client.get_image("nekos")
        embed = discord.Embed(
            colour=author.colour,
            title=f"Neko!~"
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=result.url)
        await ctx.reply(
            embed=embed,
            components = [ActionRow(
                Button(style=ButtonStyle.link, label="Source", url=f"{result.url}")
            )])
        
    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def neko2(self, ctx):
        """Neko Pictures! Pt. 2"""
        author = ctx.author
        img = await self.bot.session.get('https://nekos.life/api/v2/img/neko')
        imgtxt = await img.text()
        imgjson = json.loads(imgtxt)
        embed = discord.Embed(
            colour=author.colour,
            title = f"Neko!~"
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=imgjson["url"])
        await ctx.reply(
            embed=embed,
            components = [ActionRow(
                Button(style=ButtonStyle.red, label="Source", disabled=True)
            )])
        
    @commands.command(aliases=["ngif"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def nekogif(self, ctx):
        """Neko Gifs!"""
        author = ctx.author
        img = await self.bot.session.get('https://nekos.life/api/v2/img/ngif')
        imgtxt = await img.text()
        imgjson = json.loads(imgtxt)
        embed = discord.Embed(
            colour=author.colour,
            title = f"Neko!~"
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=imgjson["url"])
        await ctx.reply(
            embed=embed,
            components = [ActionRow(
                Button(style=ButtonStyle.red, label="Source", disabled=True)
            )])
        
    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def waifu(self, ctx):
        """Waifu Neko!"""
        author = ctx.author
        img = await self.bot.session.get('https://nekos.life/api/v2/img/waifu')
        imgtxt = await img.text()
        imgjson = json.loads(imgtxt)
        embed = discord.Embed(
            colour=author.colour,
            title = f"Waifu~"
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=imgjson["url"])
        await ctx.reply(
            embed=embed,
            components = [ActionRow(
                Button(style=ButtonStyle.red, label="Source", disabled=True)
            )])
        
    @commands.command(aliases=["nav"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @commands.cooldown(1, 5, commands.BucketType.member)
 #   @commands.bot_has_permissions(embed_links=True)
    async def nekoavatar(self, ctx):
        """
        Neko Avatar!
        [DISABLED] Too Close to Hentai.
        """
        
        author = ctx.author
        embed = discord.Embed(
        colour=author.colour,
        title = f"DISABLED.",
        description = f"This Command has potential NSFW, so to protect our kids, \n we have disabled this for now.",
        ).set_author(name=author.name, icon_url=author.avatar_url)
        await ctx.reply(embed=embed)

#       author = ctx.author
#       img = await self.bot.session.get('https://nekos.life/api/v2/img/avatar')
#       imgtxt = await img.text()
#       imgjson = json.loads(imgtxt)
#       embed = discord.Embed(
#           colour=author.colour,
#           title = f"Neko Avatar!"
#       )
#       embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
#       embed.set_image(url=imgjson["url"])
#       await ctx.reply(embed=embed)

    @commands.command(aliases=["tnav"])
    @checks.has_permissions(PermissionLevel.OWNER)
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def tnekoavatar(self, ctx):
        """
        Neko Avatar!
        But for Owner Testing
        """
        author = ctx.author
        img = await self.bot.session.get('https://nekos.life/api/v2/img/avatar')
        imgtxt = await img.text()
        imgjson = json.loads(imgtxt)
        embed = discord.Embed(
           colour=author.colour,
           title = f"Neko Avatar!"
       )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=imgjson["url"])
        await ctx.reply(
            embed=embed,
            components = [ActionRow(
                Button(style=ButtonStyle.red, label="Source", disabled=True)
            )])

def setup(bot):
    bot.add_cog(Nekos(bot))
