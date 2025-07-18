from cleanarr.filter.filter import Filter
from cleanarr.model.release import Release
from cleanarr.model.torrent import Torrent
from cleanarr.service.servarr import ServarrApi
from cleanarr.service.torrent_client import TorrentClient


class DownloadFilter:
    def __init__(self, servarrs: list[ServarrApi], torrent: TorrentClient, filter: Filter):
        self.servarrs = servarrs
        self.torrent = torrent
        self.filter = filter

    async def poll(self):
        for servarr in self.servarrs:
            releases = await servarr.get_all_downloads()
            hashes = [r['download_id'] for r in releases]
            downloads = self.torrent.get_torrents(hashes)
            for release in releases:
                download = downloads.get(release['download_id'])
                await self.filter_release(release, download, servarr)

    async def filter_release(self, release: Release, download: Torrent, servarr: ServarrApi):
        if not download:
            return
        accept, error = self.filter.test(download)
        if not accept:
            print(f'Rejected {download['name']}: {error}')
            await servarr.ban_download(release['servarr_id'])
