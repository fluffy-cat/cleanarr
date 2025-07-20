import pytest

from cleanarr.filter.extension import BlacklistExtensionFilter, WantedExtensionFilter
from cleanarr.model.torrent import Torrent, File


def test_blacklistExtensionFilter_shouldAccept_whenNoExtensionsAreBlacklisted():
    filter = BlacklistExtensionFilter([])

    accept, _ = filter.test(Torrent(files=[File(name='video.mkv')]))

    assert accept is True


def test_blacklistExtensionFilter_shouldAccept_whenThereAreNoFiles():
    filter = BlacklistExtensionFilter(['scr'])

    accept, _ = filter.test(Torrent(files=[]))

    assert accept is True


def test_blacklistExtensionFilter_shouldAccept_whenTorrentContainsNoBlacklistedExtensions():
    filter = BlacklistExtensionFilter(['scr'])

    accept, _ = filter.test(Torrent(files=[
        File(name='video.mkv'),
        File(name='release.nfo')
    ]))

    assert accept is True


def test_blacklistExtensionFilter_shouldReject_whenTorrentContainsABlacklistedExtension():
    filter = BlacklistExtensionFilter(['scr'])

    accept, error = filter.test(Torrent(files=[
        File(name='video.mkv'),
        File(name='info.scr')
    ]))

    assert accept is False
    assert error == 'Found file with blacklisted extension: info.scr'


def test_blacklistExtensionFilter_shouldAccept_whenFileHasNoExtension():
    filter = BlacklistExtensionFilter(['scr'])

    accept, error = filter.test(Torrent(files=[
        File(name='video')
    ]))

    assert accept is True


def test_wantedExtensionFilter_shouldThrowError_whenNoExtensionsAreWanted():
    with pytest.raises(ValueError) as err:
        WantedExtensionFilter([])

    assert err.value.args[0] == 'No extensions given'


def test_wantedExtensionFilter_shouldReject_whenThereAreNoFiles():
    filter = WantedExtensionFilter(['mkv', 'mp4', 'avi'])

    accept, error = filter.test(Torrent(files=[]))

    assert accept is False
    assert error == 'No files with extension found: mkv, mp4, avi'


def test_wantedExtensionFilter_shouldReject_whenThereAreNoFilesWithWantedExtensions():
    filter = WantedExtensionFilter(['mkv'])

    accept, error = filter.test(Torrent(files=[
        File(name='release.nfo')
    ]))

    assert accept is False
    assert error == 'No files with extension found: mkv'


def test_wantedExtensionFilter_shouldAccept_whenThereAreFilesWithWantedExtensions():
    filter = WantedExtensionFilter(['mkv', 'mp4', 'avi'])

    accept, _ = filter.test(Torrent(files=[
        File(name='release.nfo'),
        File(name='video.avi')
    ]))

    assert accept is True


def test_wantedExtensionFilter_shouldReject_whenFileHasNoExtension():
    filter = WantedExtensionFilter(['avi'])

    accept, error = filter.test(Torrent(files=[
        File(name='video')
    ]))

    assert accept is False
