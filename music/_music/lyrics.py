import asyncio
import os
import typing
from concurrent import futures

from lyricsgenius import Genius
from lyricsgenius.types.song import Song

from .utils import cache

__all__ = ["Lyrics"]


class Lyrics:
    def __init__(self, GENIUS_TOKEN):
        self._executor = futures.ThreadPoolExecutor(max_workers=3)
        self.GENIUS_TOKEN = GENIUS_TOKEN

    async def test_token(self) -> bool:
        loop = asyncio.get_event_loop()
        genius = Genius(self.GENIUS_TOKEN, verbose=False)
        import requests
        try:
            await loop.run_in_executor(self._executor, genius.search_song, "chevy uwu")
            return True
        except requests.exceptions.HTTPError:
            return False

    def _fetch_lyrics(self, query: str) -> typing.Optional[Song]:
        genius = Genius(self.GENIUS_TOKEN, verbose=False)
        return genius.search_song(query, get_full_info=False)

    @cache(512)
    async def fetch_lyrics(self, query: str) -> typing.Optional[Song]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._fetch_lyrics, query)
