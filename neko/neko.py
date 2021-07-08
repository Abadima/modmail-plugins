import discord,nekos,nekosbest
from discord.ext import commands
from nekosbest import Client

class Nekos(commands.cog)
    """
    Nekos!
    Thanks Abadima :D
    """

      def __init__(self, bot):
        self.bot = bot
        self.client = Client()

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def neko(self, ctx: commands.Context, user: discord.Member):
        """Picture of a Neko!"""

        author = ctx.author
        result = await self.client.get_image("nekos")

            embed = discord.Embed(colour=user.colour)
            embed.title("Neko!~")
            embed.set_image(url=result.url)
            return await ctx.reply(content=msg, embed=embed)

def setup(bot):
    bot.add_cog(Nekos(bot))
