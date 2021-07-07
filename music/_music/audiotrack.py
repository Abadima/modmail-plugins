import json
import re
from asyncio import Lock

import lavalink

from core.models import getLogger

__all__ = ["LazyAudioTrack", 'CLEAN_TITLE_RE']

logger = getLogger(__name__)
CLEAN_TITLE_RE = re.compile(r"\s*[(\[](?:official .+?|lyrics?)[)\]]", re.I)


class LazyAudioTrack(lavalink.AudioTrack):
    # noinspection PyMissingConstructor
    def __init__(self, query, title, requester: int, *, duration=None, spotify=False):
        self.requester = requester
        self.query = query
        self.og_title = self.title = CLEAN_TITLE_RE.sub("", title)
        self.spotify = spotify
        if duration:
            self.duration = duration
        self._load_lock = Lock()
        self.loaded = False
        self.success = True

    @classmethod
    def from_loaded(cls, data: dict, requester: int, **extra) -> 'LazyAudioTrack':
        self = cls(data['info']['title'], data['info']['title'], requester, **extra)
        self.loaded = True
        cls._parse_data(self, data)
        return self

    def _parse_data(self, data):
        try:
            self.track = data['track']
            self.identifier = data['info']['identifier']
            self.is_seekable = data['info']['isSeekable']
            self.author = data['info']['author']
            self.duration = data['info']['length']
            self.stream = data['info']['isStream']
            self.title = CLEAN_TITLE_RE.sub("", data['info']['title'])
            self.uri = data['info']['uri']
        except KeyError as ke:
            self.success = False
            missing_key, = ke.args
            raise lavalink.InvalidTrack('Cannot build a track from partial data! '
                                        '(Missing key: {})'.format(missing_key)) from None

    async def load(self, player):
        if self.loaded:
            return
        async with self._load_lock:
            if self.loaded:
                return
            # noinspection PyBroadException
            try:
                result = await player.req_lavalink_track(self.query)
            except Exception:
                logger.error("Fetching track failed %s", self, exc_info=True)
                self.success = False
                return
            finally:
                self.loaded = True
            if result and result['tracks']:
                self._parse_data(result['tracks'][0])
            else:
                self.success = False
                logger.error("Fetching track failed %s %s", self, result)

    def dump(self, jsonify=False):
        data = dict(
            requester=self.requester,
            query=self.query,
            og_title=self.og_title,
            title=self.title,
            spotify=self.spotify,
            duration=getattr(self, 'duration', None),
            loaded=self.loaded,
            success=self.success,
            track=getattr(self, 'track', None),
            identifier=getattr(self, 'identifier', None),
            is_seekable=getattr(self, 'is_seekable', None),
            author=getattr(self, 'author', None),
            stream=getattr(self, 'stream', None),
            uri=getattr(self, 'uri', None),
        )
        return json.dumps(data) if jsonify else data

    @classmethod
    def load_dump(cls, data) -> 'LazyAudioTrack':
        if isinstance(data, str):
            data = json.loads(data)
        self = cls(data['query'], data['title'], data['requester'], duration=data['duration'], spotify=data['spotify'])
        self.og_title = data['og_title']
        self.title = data['title']
        self.loaded = data['loaded']
        self.success = data['success']
        self.track = data['track']
        self.identifier = data['identifier']
        self.is_seekable = data['is_seekable']
        self.author = data['author']
        self.stream = data['stream']
        self.uri = data['uri']
        return self

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            if name in {'track', 'identifier', 'is_seekable', 'author', 'duration', 'stream', 'title', 'uri'}:
                raise AttributeError("Track not loaded.")
            raise

    def __repr__(self):
        if self.loaded and self.success:
            return '<AudioTrack title={0.title} identifier={0.identifier} loaded=True>'.format(self)
        return '<AudioTrack title={0.title} query={0.query} loaded=False>'.format(self)
