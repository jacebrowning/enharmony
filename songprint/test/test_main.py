#!/usr/bin/env python

"""
Unit tests for the songprint package functions.
"""

import unittest
import logging
from random import shuffle
from copy import copy

from songprint import find, match, sort, Song, Title, Artist, Album
import songprint.settings as settings

# Item lists for various tests
SONGS = [
Song("The Artists", "Song Title"),
Song("The Artists", "Song Title 2"),
Song("The Artists", "Song Title 3"),
]
TITLES = [
Title("The Song Title"),
Title("The Song Title [Live]"),
]
ARTISTS = [
Artist("The Artists"),
Artist("The Artists & Others"),
]
ALBUMS = [
Album("Album Title"),
Album("Album Title (Bonus Tracks)"),
Album("The Other Album"),
]


class TestFind(unittest.TestCase):  # pylint: disable=R0904
    """Tests against the find function."""

    def test_find_songs(self):
        """Verify songs can be found in lists."""
        for song in SONGS:
            logging.info("finding song: {0}".format(repr(song)))
            self.assertEqual(song, find(song, SONGS))

    def test_find_titles(self):
        """Verify titles can be found in lists."""
        for title in TITLES:
            logging.info("finding title: {0}".format(repr(title)))
            self.assertEqual(title, find(title, TITLES))

    def test_find_artists(self):
        """Verify artists can be found in lists."""
        for artist in ARTISTS:
            logging.info("finding artist: {0}".format(repr(artist)))
            self.assertEqual(artist, find(artist, ARTISTS))

    def test_find_albums(self):
        """Verify albums can be found in lists."""
        for album in ALBUMS:
            logging.info("finding album: {0}".format(repr(album)))
            self.assertEqual(album, find(album, ALBUMS))


class TestMatch(unittest.TestCase):  # pylint: disable=R0904
    """Tests against the match function."""

    def test_match_songs(self):
        """Verify songs can be matched in lists."""
        self.assertEqual(1, len(match(SONGS[0], SONGS)))

    def test_match_titles(self):
        """Verify titles can be matched in lists."""
        self.assertEqual(1, len(match(TITLES[0], TITLES)))

    def test_match_artists(self):
        """Verify artists can be matched in lists."""
        self.assertEqual(1, len(match(ARTISTS[0], ARTISTS)))

    def test_match_albums(self):
        """Verify albums can be matched in lists."""
        self.assertEqual(2, len(match(ALBUMS[0], ALBUMS)))


class TestSort(unittest.TestCase):  # pylint: disable=R0904
    """Tests against the sort function."""

    @unittest.expectedFailure  # TODO: support song comparison
    def test_sort_songs(self):
        """Verify a songs lists can be sorted."""
        songs = copy(SONGS)
        shuffle(songs)
        self.assertListEqual(SONGS, sort(SONGS[0], songs))

    def test_sort_titles(self):
        """Verify a titles lists can be sorted."""
        titles = copy(TITLES)
        shuffle(titles)
        self.assertListEqual(TITLES, sort(TITLES[0], titles))

    def test_sort_artists(self):
        """Verify an artists lists can be sorted."""
        artists = copy(ARTISTS)
        shuffle(artists)
        self.assertListEqual(ARTISTS, sort(ARTISTS[0], artists))

    def test_sort_albums(self):
        """Verify an albums lists can be sorted."""
        albums = copy(ALBUMS)
        shuffle(albums)
        self.assertListEqual(ALBUMS, sort(ALBUMS[0], albums))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
