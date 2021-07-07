import asyncio
import discord
from discord.ext import commands

__all__ = ['MusicError', 'QueueError', 'EndOfQueue', 'SpotifyError', 'Failure']


class MusicError(Exception):
    pass


class QueueError(MusicError):
    pass


class EndOfQueue(QueueError):
    pass


# Some issue retrieving something from Spotify's API
class SpotifyError(MusicError):
    pass


class Failure(commands.CommandError):
    def __init__(self, ctx, message):
        asyncio.create_task(ctx.send(embed=discord.Embed(
            description=message,
            colour=discord.Colour.red()
        )))
        super().__init__(message)
