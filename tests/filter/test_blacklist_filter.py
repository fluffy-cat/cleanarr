from unittest.mock import Mock

from cleanarr.filter.blacklist import BlacklistFilter
from cleanarr.model.torrent import Torrent


def test_shouldAccept_whenFilterListIsEmpty():
    download = Torrent()
    blacklist = BlacklistFilter([])

    result = blacklist.test(download)

    assert result == (True, '')


def test_shouldAccept_whenAllChildFiltersPass():
    download = Torrent()
    filter1 = Mock()
    filter1.test.return_value = (True, '')
    filter2 = Mock()
    filter2.test.return_value = (True, '')
    blacklist = BlacklistFilter([filter1, filter2])

    result = blacklist.test(download)

    assert filter1.test.called
    assert filter2.test.called
    assert result == (True, '')


def test_shouldRejectAndEndChecks_whenFirstChildFilterFails():
    download = Torrent()
    filter1 = Mock()
    filter1.test.return_value = (False, 'reason')
    filter2 = Mock()
    filter2.test.return_value = (True, 'ignored')
    blacklist = BlacklistFilter([filter1, filter2])

    result = blacklist.test(download)

    assert result == (False, 'reason')
    assert not filter2.test.called
