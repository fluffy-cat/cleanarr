import transmission_rpc
from transmission_rpc import Client

from cleanarr.model.torrent import Torrent, File, TorrentState


class TorrentClient:
    def __init__(self, client: Client):
        self.client = client

    def get_torrents(self, hashes: list[str]) -> dict[str, Torrent]:
        torrents = [to_torrent(t) for h in hashes for t in self.client.get_torrents(h)]
        return {t['hash']: t for t in torrents}


def to_torrent(torrent: transmission_rpc.Torrent):
    files = [File(name=f.name) for f in torrent.get_files()]
    state = to_torrent_state(torrent)
    return Torrent(name=torrent.name, hash=torrent.hash_string, state=state, files=files)


def to_torrent_state(torrent: transmission_rpc.Torrent):
    if torrent.metadata_percent_complete < 1:
        return TorrentState.INITIALISING
    elif torrent.percent_done < 1:
        return TorrentState.DOWNLOADING
    else:
        return TorrentState.DONE
