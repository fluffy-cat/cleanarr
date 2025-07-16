from typing import Any

import aiohttp
from aiohttp import ClientResponse

from cleanarr.servarr import ServarrApi


class RadarrApi(ServarrApi):
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key

    async def get_all_downloads(self) -> dict[str, Any]:
        url = f'{self.url}/api/v3/queue?page=1&pageSize=100&includeUnknownMovieItems=false'
        async with aiohttp.request('GET',
                                   url,
                                   headers=self.get_auth_header()) as res:
            return await self.parse_all_downloads(res)

    async def parse_all_downloads(self, res: ClientResponse) -> dict[str, Any]:
        if res.status != 200:
            raise RuntimeError(f'Failed to get all downloads from {self.url}. Code {res.status}')
        else:
            return await res.json()

    async def ban_download(self, id: int):
        url = f'{self.url}/api/v3/queue/bulk?removeFromClient=true&blocklist=true&skipRedownload=false&changeCategory=false'
        async with aiohttp.request('DELETE',
                                   url,
                                   headers=self.get_auth_header(),
                                   json=make_ban_download_request(id)) as res:
            return await self.parse_ban_download(res, id)

    async def parse_ban_download(self, res: ClientResponse, id: int) -> dict[str, Any]:
        if res.status != 200:
            raise RuntimeError(f'Failed to ban download id {id} at {self.url}. Code {res.status}')
        else:
            return {}

    def get_auth_header(self):
        return {
            'X-Api-Key': self.api_key
        }


def make_ban_download_request(id: int) -> dict[str, Any]:
    return {
        'ids': [
            id
        ]
    }
