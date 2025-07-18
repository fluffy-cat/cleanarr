from cleanarr.model.torrent import Torrent


class Filter:
    def test(self, download: Torrent) -> tuple[bool, str]:
        return True, ''
