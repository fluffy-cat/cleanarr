import asyncio
import traceback
from collections.abc import Callable
from datetime import timedelta
from typing import Any

import transmission_rpc
import yaml

from cleanarr.api.radarr import RadarrApi
from cleanarr.api.sonarr import SonarrApi
from cleanarr.controller.download_filter import DownloadFilter
from cleanarr.filter.blacklist import BlacklistFilter
from cleanarr.filter.extension import BlacklistExtensionFilter, WantedExtensionFilter
from cleanarr.filter.filter import Filter
from cleanarr.service.radarr import Radarr
from cleanarr.service.servarr import ServarrApi
from cleanarr.service.sonarr import Sonarr
from cleanarr.service.torrent_client import TorrentClient


def new_sonarr(config: dict[str, Any]) -> ServarrApi:
    repo = SonarrApi(config['url'], config['api_key'])
    return Sonarr(repo)


def new_radarr(config: dict[str, Any]) -> ServarrApi:
    repo = RadarrApi(config['url'], config['api_key'])
    return Radarr(repo)


def new_downloader(config: dict[str, Any]) -> TorrentClient:
    client = transmission_rpc.from_url(config['url'])
    return TorrentClient(client)


def new_filter(config: dict[str, Any]) -> Filter:
    blacklist = BlacklistExtensionFilter(config['blacklisted_files'])
    wanted = WantedExtensionFilter(config['wanted_files'])
    return BlacklistFilter([blacklist, wanted])


def new_download_filter_controller(config: dict[str, Any],
                                   servarr: list[ServarrApi],
                                   downloader: TorrentClient) -> DownloadFilter:
    filter = new_filter(config)
    return DownloadFilter(servarr, downloader, filter)


def new_download_filter_task(config: dict[str, Any], servarr: list[ServarrApi], downloader: TorrentClient):
    download_filter = new_download_filter_controller(config, servarr, downloader)
    poll_interval = timedelta(seconds=config['poll_interval_s'])
    return new_periodic_task(download_filter.run, poll_interval)


async def new_periodic_task(callable: Callable[[], Any], interval: timedelta):
    while True:
        await callable()
        await asyncio.sleep(interval.total_seconds())


def main():
    with open('application.yml', 'r') as file:
        config = yaml.safe_load(file)
    sonarr = new_sonarr(config['sonarr'])
    radarr = new_radarr(config['radarr'])
    servarr = [sonarr, radarr]
    downloader = new_downloader(config['transmission'])
    download_filter_task = new_download_filter_task(config['download_filter'], servarr, downloader)
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(download_filter_task)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'Uncaught exception found {e} {traceback.format_exc()}')


if __name__ == "__main__":
    main()
