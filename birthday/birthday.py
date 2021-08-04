import asyncio, datetime, discord, logging, pytz

from difflib import get_close_matches
from discord.ext import commands
from pytz import timezone

from core import checks
from core.models import PermissionLevel

logger = logging.getLogger("Modmail")


class Birthdays(commands.Cog):
    """
    Birthdays :D
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.birthdays = dict()
        self.roles = dict()
        self.channels = dict()
        self.timezone = "America/Chicago"
        self.messages = dict()
        self.enabled = True
        self.booted = True
        self.bot.loop.create_task(self._set_db())

    async def _set_db(self):
        birthdays = await self.db.find_one({"_id": "birthdays"})
        config = await self.db.find_one({"_id": "config"})

        if birthdays is None:
            await self.db.find_one_and_update(
                {"_id": "birthdays"}, {"$set": {"birthdays": dict()}}, upsert=True
            )

            birthdays = await self.db.find_one({"_id": "birthdays"})

        if config is None:
            await self.db.find_one_and_update(
                {"_id": "config"},
                {
                    "$set": {
                        "roles": dict(),
                        "channels": dict(),
                        "enabled": True,
                        "timezone": "America/Chicago",
                        "messages": dict(),
                    }
                },
                upsert=True,
            )

            config = await self.db.find_one({"_id": "config"})

        self.birthdays = birthdays.get("birthdays", dict())
        self.roles = config.get("roles", dict())
        self.channels = config.get("channels", dict())
        self.enabled = config.get("enabled", True)
        self.timezone = config.get("timezone", "America/Chicago")
        self.messages = config.get("messages", dict())
        self.bot.loop.create_task(self._handle_birthdays())

    async def _update_birthdays(self):
        await self.db.find_one_and_update(
            {"_id": "birthdays"}, {"$set": {"birthdays": self.birthdays}}, upsert=True
        )

    async def _update_config(self):
        await self.db.find_one_and_update(
            {"_id": "config"},
            {
                "$set": {
                    "roles": self.roles,
                    "channels": self.channels,
                    "enabled": self.enabled,
                    "timezone": self.timezone,
                    "messages": self.messages,
                }
            },
            upsert=True,
        )

    async def _handle_birthdays(self):
        while True:
            if not self.enabled:
                return

            if self.booted:
                custom_timezone = timezone(self.timezone)
                now = datetime.datetime.now(custom_timezone)
                sleep_time = (
                    now.replace(hour=0, minute=15, second=0, microsecond=0) - now
                ).seconds
                self.booted = False
                await asyncio.sleep(sleep_time)
                continue

            today = now.strftime("%d/%m/%Y").split("/")

            for user, obj in self.birthdays.items():
                if obj["month"] != today[1] or obj["day"] != today[0]:
                    continue
                guild = self.bot.get_guild(int(obj["guild"]))
                if guild is None:
                    continue
                member = guild.get_member(int(user))
                if member is None:
                    continue

                if self.roles[obj["guild"]]:
                    role = guild.get_role(int(self.roles[obj["guild"]]))
                    if role:
                        await member.add_roles(role, reason="Birthday Boi")

                if self.messages[obj["guild"]] and self.channels[obj["guild"]]:
                    channel = guild.get_channel(int(self.channels[obj["guild"]]))
                    if channel is None:
                        continue
                    age = today[2] - obj["year"]
                    await channel.send(
                        self.messages[obj["guild"]]
                        .replace("{user.mention}", member.mention)
                        .replace("{user}", str(member))
                        .replcae("{age}", age)
                    )
                    continue

            custom_timezone = timezone(self.timezone)
            now = datetime.datetime.now(custom_timezone)
            sleep_time = (
                now.replace(hour=0, minute=0, second=0, microsecond=0) - now
            ).seconds
            await asyncio.sleep(sleep_time)

    @commands.group(invoke_without_command=True)
    async def birthday(self, ctx: commands.Context):
        """
        Birthday stuff.
        """

        await ctx.send_help(ctx.command)
        return

    @birthday.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def set(self, ctx: commands.Context, date: str):
        """
        Setup your Birthday
        **Format:**
        DD/MM/YYYY
        **Example:**
        {p}birthday set 15/12/2006
        """

        try:
            birthday = date.split("/")
            if int(birthday[1]) > 13:
                await ctx.send(":x: | Invalid month provided.")
                return
            birthday_obj = {}
            birthday_obj["day"] = int(birthday[0])
            birthday_obj["month"] = int(birthday[1])
            birthday_obj["year"] = int(birthday[2])
            birthday_obj["guild"] = str(ctx.guild.id)

            self.birthdays[str(ctx.author.id)] = birthday_obj
            await self._update_birthdays()
            await ctx.send(f"Done! Your birthday was set to {date}")
            return
        except KeyError:
            logger.info(birthday[0])
            logger.info(birthday[1])
            logger.info(birthday[2])

            await ctx.send("Please check the format of the date")
            return
        except Exception as e:
            await ctx.send(f":x: | An error occurred\n```{e}```")
            return

    @birthday.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def clear(self, ctx: commands.Context):
        """
        Clear your birthday from the database.
        """

        self.birthdays.pop(str(ctx.author.id))
        await self._update_birthdays()
        await ctx.send(f"Done!")
        return

    @birthday.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """
        Configure a channel for sending birthday announcements
        """

        self.channels[str(ctx.guild.id)] = str(channel.id)
        await self._update_config()
        await ctx.send("Done!")
        return

    @birthday.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def role(self, ctx: commands.Context, role: discord.Role):
        """
        Birthday Role!
        """

        self.roles[str(ctx.guild.id)] = str(role.id)
        await self._update_config()
        await ctx.send("Done!")
        return

    @birthday.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def message(self, ctx: commands.Context, *, msg: str):
        """
        Announce Birthday Message!
        **Formatting:**
        • {user} - Their Name
        • {user.mention} - Mention DaBirthday Person
        • {age} - Age of Birthday Person
        """

        self.messages[str(ctx.guild.id)] = msg
        await self._update_config()
        await ctx.send("Done!")
        return

    @birthday.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def toggle(self, ctx: commands.Context):
        """
        Enable/Disable Birthdays
        """

        self.enabled = not self.enabled
        await self._update_config()
        await ctx.send(f"{'Enabled' if self.enabled else 'Disabled'} the plugin :p")
        return

    @birthday.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def timezone(self, ctx: commands.Context, timezone: str):
        """
        Timezone
        """

        if timezone not in pytz.all_timezones:
            matches = get_close_matches(timezone, pytz.all_timezones)
            if len(matches) > 0:
                embed = discord.Embed()
                embed.color = 0xEB3446
                embed.description = f"Did you mean: \n`{'`, `'.join(matches)}`"
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send("Couldn't find the timezone.")
                return

        self.timezone = timezone
        await self._update_config()
        await ctx.send("Done")
        return


def setup(bot):
    bot.add_cog(Birthdays(bot))
