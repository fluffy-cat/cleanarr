from cleanarr.service.servarr import ServarrApi
from cleanarr.service.torrent_client import TorrentClient


class DownloadFilter:
    def __init__(self, servarrs: list[ServarrApi], torrent: TorrentClient):
        self.servarrs = servarrs
        self.torrent = torrent

    async def poll(self):
        for servarr in self.servarrs:
            downloads = await servarr.get_all_downloads()
            for release in downloads:
                pass