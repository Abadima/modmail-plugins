import re as _re

from .audiotrack import *
from .exceptions import *
from ._player import Player
from .queue import Queue
from .spotify import *
from .lyrics import *
from . import utils
from .utils import *

URL_REGEX = _re.compile(r'(https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.'
                        r'[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*))', _re.I)
YOUTUBE_REGEX = _re.compile(r'youtube\.com|youtu\.be', _re.I)
IDENTIFIER_REGEX = _re.compile(r'^(scsearch:|ytsearch:|spotify:)')
DURATION_REGEX = _re.compile(r"(?:(?P<hours>\d+(?:\.\d+)?)h)?"
                             r"(?:(?P<minutes>\d+(?:\.\d+)?)m)?"
                             r"(?:(?P<seconds>\d+(?:\.\d+)?)s)?",
                             _re.I)
