"""
This module contains unit tests for the playlist song remove function.

Test cases:
- testAdd: test that the RemoveSongFromPlaylist function removes a song from a playlist correctly
"""
import unittest
import json
from databasefunctions import RemoveSongFromPlaylist, AddSongtoPlaylist


class TestingPlaylistSongRemoveFunction(unittest.TestCase):
    """
    Test cases for the RemoveSongFromPlaylist function.

    Functions:
    - testAdd: test that the RemoveSongFromPlaylist 
    function removes a song from a playlist correctly
    """
    # pylint: disable=invalid-name
    def testRemove(self):
        """
        Test that the RemoveSongFromPlaylist function removes a song from a playlist correctly.

        Input:
        - a playlist with four songs
        - the ID, name, and artist of a song to be removed from the playlist

        Output:
        - an updated playlist without the song that was removed
        """
        # creating a playlist
        songs = '''[
            {
                "songID": 1,
                "songResult": "Song 1",
                "artistResult": "Artist 1"
            },
            {
                "songID": 2,
                "songResult": "Song 2",
                "artistResult": "Artist 2"
            },
            {
                "songID": 3,
                "songResult": "Song 3",
                "artistResult": "Artist 3"
            },
            {
                "songID": 4,
                "songResult": "Song 4",
                "artistResult": "Artist 4"
            }
        ]'''

        songID = 2
        songResult = "Song 2"
        artistResult = "Artist 2"

        # Call the function to be tested
        updated_songs = RemoveSongFromPlaylist(
            songs, songID, songResult, artistResult)

        # Convert the updated songs back to a list
        updated_songs_list = json.loads(updated_songs)

        # Check that the song with songID 2 was removed from the playlist
        self.assertEqual(len(updated_songs_list), 3)
        self.assertNotIn({"songID": 2, "songResult": "Song 2",
                         "artistResult": "Artist 2"}, updated_songs_list)

        # Check that the remaining songs are still in the playlist
        self.assertIn({"songID": 1, "songResult": "Song 1",
                      "artistResult": "Artist 1"}, updated_songs_list)
        self.assertIn({"songID": 3, "songResult": "Song 3",
                      "artistResult": "Artist 3"}, updated_songs_list)
        self.assertIn({"songID": 4, "songResult": "Song 4",
                      "artistResult": "Artist 4"}, updated_songs_list)

class TestingAddSongtoPlaylistFunction(unittest.TestCase):
    def testAdd(self):
        # creating a playlist
        songs = '''[
            {
                "songID": 1,
                "songResult": "Song 1",
                "artistResult": "Artist 1"
            },
            {
                "songID": 2,
                "songResult": "Song 2",
                "artistResult": "Artist 2"
            },
            {
                "songID": 3,
                "songResult": "Song 3",
                "artistResult": "Artist 3"
            },
            {
                "songID": 4,
                "songResult": "Song 4",
                "artistResult": "Artist 4"
            }
        ]'''
        
        songID = 5
        songResult = "Song 5"
        artistResult = "Artist 5"

        # Call the function to be tested
        updated_songs = AddSongtoPlaylist(
            songs, songID, songResult, artistResult)

        # Convert the updated songs back to a list
        updated_songs_list = json.loads(updated_songs)

        # Check that the song with songID 2 was added to the playlist
        self.assertEqual(len(updated_songs_list), 5)
        self.assertIn({"songID": 5, "songResult": "Song 5",
                         "artistResult": "Artist 5"}, updated_songs_list)

        # Check that the remaining songs are still in the playlist
        self.assertIn({"songID": 1, "songResult": "Song 1",
                      "artistResult": "Artist 1"}, updated_songs_list)
        self.assertIn({"songID": 2, "songResult": "Song 2",
                      "artistResult": "Artist 2"}, updated_songs_list)
        self.assertIn({"songID": 3, "songResult": "Song 3",
                      "artistResult": "Artist 3"}, updated_songs_list)
        self.assertIn({"songID": 4, "songResult": "Song 4",
                      "artistResult": "Artist 4"}, updated_songs_list)

if __name__ == '__main__':
    unittest.main()
