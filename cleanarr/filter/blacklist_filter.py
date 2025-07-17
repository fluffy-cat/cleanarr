from cleanarr.filter.Filter import Filter
from cleanarr.model.torrent import Torrent


class BlacklistFilter(Filter):
    def __init__(self, filters: list[Filter]):
        self.filters = filters

    def test(self, download: Torrent) -> tuple[bool, str]:
        for f in self.filters:
            result = f.test(download)
            if not result[0]:
                return result
        return (True, '')
