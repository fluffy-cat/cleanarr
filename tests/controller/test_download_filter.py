from unittest.mock import Mock, AsyncMock

import pytest

from cleanarr.controller.download_filter import DownloadFilter
from cleanarr.model.release import Release


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
def controller(servarrs, downloader):
    return DownloadFilter(servarrs, downloader)


async def test_shouldDoNothing_whenThereAreNoServarrs(controller, servarrs, radarr):
    servarrs.clear()

    await controller.poll()

    assert not radarr.get_all_downloads.called
    assert not radarr.ban_download.called


async def test_shouldDoNothing_whenThereAreNoDownloads(controller, servarrs, radarr):
    radarr.get_all_downloads.return_value = []

    await controller.poll()

    assert radarr.get_all_downloads.called
    assert not radarr.ban_download.called


async def test_shouldAcceptDownload_whenThereAreNoFilters(controller, servarrs, radarr):
    radarr.get_all_downloads.return_value = [Release(servarr_id=123, download_id='')]

    await controller.poll()

    assert not radarr.ban_download.called
