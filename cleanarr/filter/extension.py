from cleanarr.filter.filter import Filter
from cleanarr.model.torrent import Torrent


class BlacklistExtensionFilter(Filter):
    def __init__(self, extensions: list[str]):
        self.extensions = extensions

    def test(self, download: Torrent) -> tuple[bool, str]:
        for file in download['files']:
            ext = file['name'].split('.')[-1]
            if ext in self.extensions:
                return (False, f'Found file with blacklisted extension: {file["name"]}')
        return True, ''

class WantedExtensionFilter(Filter):
    def __init__(self, extensions: list[str]):
        self.extensions = extensions

    def test(self, download: Torrent) -> tuple[bool, str]:
        # for file in download['files']:
        #     ext = file['name'].split('.')[-1]
        #     if ext in self.extensions:
        #         return (False, f'Found file with blacklisted extension: {file["name"]}')
        return True, ''