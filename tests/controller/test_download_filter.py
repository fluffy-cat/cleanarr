from unittest.mock import Mock, AsyncMock

import pytest

from cleanarr.controller.download_filter import DownloadFilter
from cleanarr.model.release import Release
from cleanarr.model.torrent import Torrent


@pytest.fixture
def radarr():
    return AsyncMock()


@pytest.fixture
def servarrs(radarr):
    return [radarr]


@pytest.fixture
def downloader():
    return Mock()


@pytest.fixture
def filter():
    return Mock()


@pytest.fixture
def controller(servarrs, downloader, filter):
    return DownloadFilter(servarrs, downloader, filter)


async def test_shouldDoNothing_whenThereAreNoServarrs(controller, servarrs, radarr):
    servarrs.clear()

    await controller.run()

    assert not radarr.get_all_downloads.called
    assert not radarr.ban_download.called


async def test_shouldDoNothing_whenThereAreNoReleases(controller, radarr):
    radarr.get_all_downloads.return_value = []

    await controller.run()

    assert radarr.get_all_downloads.called
    assert not radarr.ban_download.called


async def test_shouldAcceptDownload_whenFilterReturnsTrue(controller, radarr, filter):
    radarr.get_all_downloads.return_value = [Release(servarr_id=123, download_id='')]
    filter.test.return_value = (True, '')

    await controller.run()

    assert not radarr.ban_download.called


async def test_shouldRejectDownload_whenFilterReturnsFalse(controller, radarr, filter, downloader):
    radarr.get_all_downloads.return_value = [Release(servarr_id=123, download_id='111')]
    downloader.get_torrents.return_value = {'111': Torrent(name='Some Thing')}
    filter.test.return_value = (False, 'Denied!')

    await controller.run()

    radarr.ban_download.assert_called_with(123)


async def test_shouldIgnoreDownload_whenTorrentIsNotFound(controller, radarr, downloader):
    radarr.get_all_downloads.return_value = [Release(servarr_id=123, download_id='111')]
    downloader.get_torrents.return_value = {}

    await controller.run()

    assert not radarr.ban_download.called

async def test_shouldIgnoreDownload_whenDownloadIdIsMissing(controller, radarr, downloader):
    radarr.get_all_downloads.return_value = [Release(servarr_id=1, download_id='')]
    downloader.get_torrents.return_value = {}

    await controller.run()

    assert not radarr.ban_download.called