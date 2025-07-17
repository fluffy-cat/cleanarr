from typing import Any

from cleanarr.api.radarr import RadarrApi
from cleanarr.model.release import Release
from cleanarr.service.servarr import ServarrApi


class Radarr(ServarrApi):
    def __init__(self, radarr: RadarrApi):
        self.radarr = radarr

    async def get_all_downloads(self) -> list[Release]:
        res = await self.radarr.get_all_downloads()
        return [to_release(r) for r in res['records']]

    async def ban_download(self, id: int):
        return await self.radarr.ban_download(id)


def to_release(record: dict[str, Any]) -> Release:
    return Release(servarr_id=record['id'], download_id=record['downloadId'])
