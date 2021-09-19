import datetime
import discord
from discord import Embed, Guild, Member, Role
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context, Greedy, group
from discord.utils import get

class TicketManagement(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @group(name="ticket", invoke_without_command=True)
    async def ticket(self, ctx: Context) -> None:
        """Open and close a ticket or submit a DM for Support."""
        await ctx.send_help(ctx.command)

    @ticket.command(name="open")
    async def open(self, ctx: Context, user: discord.Member):
        """Open a ticket for the specified user"""
        # Embed
        embed = discord.Embed(title="**Support Request Accepted**", description=f"Hey <@{user.id}>, your request has been accepted and for this we have opened a ticket. the team will get back to you as soon as possible.", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.add_field(name="**FAQ**", value=f"Coming Soon", inline=False)
        embed.add_field(name="**Bulletin Board**", value=f"Testing", inline=False)
        embed2 = discord.Embed(title="**Open Support Request**", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed2.set_author(name=user.name, icon_url=user.avatar_url)
        embed2.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed2.add_field(name="Staff", value=f"{ctx.author.mention} | ID: {ctx.author.id}", inline=False)
        embed2.add_field(name="User", value=f"{user.mention} | ID: {user.id}", inline=False)
        # Vars
        userchannel = None
        mod = get(ctx.guild.roles, id=747328846457733150)
        category = get(ctx.guild.channels, id=889238124964745317)
        channel_log = get(ctx.guild.channels, id=889238600783392769)
        # Channel Check
        for channel in ctx.guild.text_channels:
                if channel.topic == f"Ticket User ID: {str(user.id)}":
                        userchannel = channel
	# Ticket Open
        if userchannel == None:
                print(f"No Ticket Channel detected for {user.name}")
                channel = await ctx.guild.create_text_channel(f"ticket-{user.name}", category=category, topic=f"Ticket User ID: {str(user.id)}")
                await channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
                await channel.set_permissions(mod, read_messages=True, send_messages=True, manage_messages=True, embed_links=True, attach_files=True)
                await channel.set_permissions(user, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True)
                await channel.send(embed=embed)
                await ctx.send(f"**Open ticket for {user.mention} ('{str(user.id)}')**")
                await channel_log.send(embed=embed2)
        else:
                await ctx.send(f"The user {user.mention} ('{str(user.id)}') already has a ticket open.")
                print(f"Ticket Channel detected for {user.name}")
        
    @ticket.command(name="close")
    async def close(self, ctx: Context, check: discord.User, *, reason: str):
        """Close a ticket for the specified user"""
        user = ctx.guild.get_member(check.id)
        if user == None:
        	if reason.lower() == "force":
        		forcechannel = None
        		forceembed = discord.Embed(description=f"Channel Forcefully Closed.", color=discord.Color.red())
        		for channel in ctx.guild.text_channels:
        			if channel.topic == f"Ticket User ID: {str(check.id)}":
        				forcechannel = channel
			# Force Close
        		if forcechannel == None:
        			await ctx.send(f"The user does not have any open tickets that can be forced.")
        		else:
        			await forcechannel.delete()
        			await ctx.send(embed=discord.Embed(description=f"Channel Forcefully Closed.", color=discord.Color.red()))
        	else:
        		await ctx.send(embed=discord.Embed(description=f"The user is not **member** of the server!", color=discord.Color.red()))
        else:
        	# Embed
        	embed2 = discord.Embed(title="**Support Request Closed**", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        	embed2.set_author(name=user.name, icon_url=user.avatar_url)
        	embed2.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        	embed2.add_field(name="Staff", value=f"{ctx.author.mention} | ID: {ctx.author.id}", inline=False)
        	embed2.add_field(name="Reason", value=reason, inline=False)
        	embed3 = discord.Embed(title="**Support Request Closed**", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        	embed3.set_author(name=user.name, icon_url=user.avatar_url)
        	embed3.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        	embed3.add_field(name="Staff", value=f"{ctx.author.mention} | ID: {ctx.author.id}", inline=False)
        	embed3.add_field(name="User", value=f"{user.mention} | ID: {user.id}", inline=False)
        	embed3.add_field(name="Reason", value=reason, inline=False)
        	# Vars
        	userchannel = None
        	channel_log = get(ctx.guild.channels, id=889238600783392769)
		# Channel Check
        	for channel in ctx.guild.text_channels:
        		if channel.topic == f"Ticket User ID: {str(user.id)}":
        			userchannel = channel
        			print(f"Ticket Channel detected for {user.name}")
        	# Ticket Close
        	if userchannel == None:
        		await ctx.send(f"The user {user.mention} ('{str(user.id)}') has no open ticket.")
        		print(f"No Ticket Channel detected for {user.name}")
        	else:
        		print(f"Ticket Channel detected for {user.name}")
        		await userchannel.delete()
        		await ctx.send(f"**Ticket closed for {user.mention} ('{str(user.id)}') with reason: '{reason}'**")
        		await channel_log.send(embed=embed3)
        		await user.send(embed=embed2)
                
    @ticket.command(name="dm")
    async def dm(self, ctx: Context, user: discord.Member, *, content: str):
        """Send a DM to the specified user"""
        #Vars
        channel_log = get(ctx.guild.channels, id=889238600783392769)
        # Embed
        embed3 = discord.Embed(title="**Support Request Notification**", color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed3.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed3.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed3.add_field(name="Staff", value=f"{ctx.author.mention} | ID: {ctx.author.id}", inline=False)
        embed3.add_field(name="Message", value=content, inline=False)
        embed4 = discord.Embed(title="**Send DM Message**", color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed4.set_author(name=user.name, icon_url=user.avatar_url)
        embed4.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed4.add_field(name="Staff", value=f"{ctx.author.mention} | ID: {ctx.author.id}", inline=False)
        embed4.add_field(name="User", value=f"{user.mention} | ID: {user.id}", inline=False)
        embed4.add_field(name="Message", value=content, inline=False)
        # DM
        try:
                await user.send(embed=embed3)
                await ctx.send(embed=embed4)
                await channel_log.send(embed=embed4)
        except:
                await ctx.send(f"User {user.mention} ('{str(user.id)}') does not accept private messages (DM).")
        
def setup(bot):
    bot.add_cog(TicketManagement(bot))
