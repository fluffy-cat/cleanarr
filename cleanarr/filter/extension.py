from cleanarr.filter.filter import Filter
from cleanarr.model.torrent import Torrent, File


class BlacklistExtensionFilter(Filter):
    def __init__(self, extensions: list[str]):
        self.extensions = extensions

    def test(self, download: Torrent) -> tuple[bool, str]:
        for file in download['files']:
            ext = parse_extension(file)
            if ext in self.extensions:
                return False, f'Found file with blacklisted extension: {file["name"]}'
        return True, ''


class WantedExtensionFilter(Filter):
    def __init__(self, extensions: list[str]):
        if not extensions:
            raise ValueError('No extensions given')
        self.extensions = extensions

    def test(self, download: Torrent) -> tuple[bool, str]:
        for file in download['files']:
            ext = parse_extension(file)
            if ext in self.extensions:
                return True, ''
        return False, f'No files with extension found: {", ".join(self.extensions)}'


def parse_extension(file: File) -> str:
    ext = file['name'].split('.')[-1]
    return ext
