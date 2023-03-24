import unittest
import json
from databasefunctions import RemoveSongFromPlaylist


class TestingPlaylistSongRemoveFunction(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
