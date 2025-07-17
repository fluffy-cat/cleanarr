from unittest.mock import Mock

import pytest

from cleanarr.model.torrent import TorrentState
from cleanarr.service.torrent_client import TorrentClient


@pytest.fixture
def transmission():
    return Mock()


@pytest.fixture
def client(transmission):
    return TorrentClient(transmission)


async def test_shouldReturnEmptyDict_whenThereAreNoTorrents(client, transmission):
    transmission.get_torrents.return_value = []

    output = client.get_torrents([''])

    assert len(output) == 0


async def test_shouldPopulateTorrentAttributes(client, transmission):
    torrent1 = Mock()
    torrent1.name = 'my torrent'
    torrent1.hash_string = '96e27060c265a505ef722dc9405c32b211f3b5a9'
    torrent1.metadata_percent_complete = 0.99
    file = Mock()
    file.name = 'my file.exe'
    torrent1.get_files.return_value = [file]
    torrent2 = Mock()
    torrent2.name = 'torrent 2'
    torrent2.hash_string = '2'
    torrent2.metadata_percent_complete = 0.99
    torrent2.get_files.return_value = []
    transmission.get_torrents.return_value = [torrent1, torrent2]

    output = client.get_torrents([''])

    assert len(output) == 2
    out = output['96e27060c265a505ef722dc9405c32b211f3b5a9']
    assert out['name'] == 'my torrent'
    assert out['hash'] == '96e27060c265a505ef722dc9405c32b211f3b5a9'
    assert out['files'][0]['name'] == 'my file.exe'
    out = output['2']
    assert out['name'] == 'torrent 2'
    assert out['hash'] == '2'
    assert len(out['files']) == 0


async def test_shouldBeInInitialisingState_whenMetadataPercentageIsLessThan1(client, transmission):
    torrent = Mock()
    torrent.hash_string = '0'
    torrent.get_files.return_value = []
    torrent.metadata_percent_complete = 0.99
    transmission.get_torrents.return_value = [torrent]

    output = client.get_torrents([''])

    assert output['0']['state'] == TorrentState.INITIALISING


async def test_shouldBeInDownloadingState_whenMetadataPercentageIs1AndPercentageDoneIsLessThan1(client, transmission):
    torrent = Mock()
    torrent.hash_string = '0'
    torrent.get_files.return_value = []
    torrent.metadata_percent_complete = 1
    torrent.percent_done = 0.99
    transmission.get_torrents.return_value = [torrent]

    output = client.get_torrents([''])

    assert output['0']['state'] == TorrentState.DOWNLOADING


async def test_shouldBeInDoneState_whenMetadataPercentageIs1AndPercentageDoneIs1(client, transmission):
    torrent = Mock()
    torrent.hash_string = '0'
    torrent.get_files.return_value = []
    torrent.metadata_percent_complete = 1
    torrent.percent_done = 1
    transmission.get_torrents.return_value = [torrent]

    output = client.get_torrents([''])

    assert output['0']['state'] == TorrentState.DONE
