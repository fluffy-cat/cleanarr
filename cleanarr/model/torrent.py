from enum import auto, Enum
from typing import TypedDict


class TorrentState(Enum):
    INITIALISING = auto()
    DOWNLOADING = auto()
    PAUSED = auto()
    DONE = auto()


class File(TypedDict):
    name: str


class Torrent(TypedDict):
    name: str
    hash: str
    state: TorrentState
    files: list[File]
