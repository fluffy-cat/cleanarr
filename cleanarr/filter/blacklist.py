from cleanarr.filter.filter import Filter
from cleanarr.model.torrent import Torrent


class BlacklistFilter(Filter):
    def __init__(self, filters: list[Filter]):
        self.filters = filters

    def test(self, download: Torrent) -> tuple[bool, str]:
        for f in self.filters:
            accept, error = f.test(download)
            if not accept:
                return accept, error
        return True, ''
