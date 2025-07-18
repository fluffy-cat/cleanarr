from cleanarr.filter.extension import BlacklistExtensionFilter
from cleanarr.model.torrent import Torrent, File


def test_blacklistExtensionFilter_shouldAccept_whenNoExtensionsAreBlacklisted():
    filter = BlacklistExtensionFilter([])

    result, _ = filter.test(Torrent(files=[File(name='video.mkv')]))

    assert result is True


def test_blacklistExtensionFilter_shouldAccept_whenThereAreNoFiles():
    filter = BlacklistExtensionFilter(['scr'])

    result, _ = filter.test(Torrent(files=[]))

    assert result is True


def test_blacklistExtensionFilter_shouldAccept_whenTorrentContainsNoBlacklistedExtensions():
    filter = BlacklistExtensionFilter(['scr'])

    result, _ = filter.test(Torrent(files=[
        File(name='video.mkv'),
        File(name='release.nfo')
    ]))

    assert result is True


def test_blacklistExtensionFilter_shouldReject_whenTorrentContainsABlacklistedExtension():
    filter = BlacklistExtensionFilter(['scr'])

    result, msg = filter.test(Torrent(files=[
        File(name='video.mkv'),
        File(name='info.scr')
    ]))

    assert result is False
    assert msg == 'Found file with blacklisted extension: info.scr'


def test_blacklistExtensionFilter_shouldAccept_whenFileHasNoExtension():
    filter = BlacklistExtensionFilter(['scr'])

    result, msg = filter.test(Torrent(files=[
        File(name='video')
    ]))

    assert result is True
