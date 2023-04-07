"""
This module contains functions for manipulating data in the database.

Functions:
- AddSongtoPlaylist: add a song to a playlist
- RemoveSongFromPlaylist: remove a song from a playlist
- AddSharedUserByPlaylistCreator: add a shared user to a playlist
"""

import json

# pylint: disable=invalid-name
def AddSongtoPlaylist(songs, songID, songResult, artistResult, imageURL):
    """
    Takes the json string from playlist.songs
    songID, songResult, artistResult, imageURL of the song to be added

    first converts it into python dict
    then adds the song
    then converts it backs to the string

    retuns songs as string

    """
    new_songs = json.loads(songs)
    song = {
        "songID": songID,
        "songResult": songResult,
        "artistResult": artistResult,
        "imageURL": imageURL
    }

    new_songs.append(song)
    songs = json.dumps(new_songs)

    return songs

def RemoveSongFromPlaylist(songs, songID, songResult, artistResult, imageURL):
    """
    Takes the json string from playlist.songs
    songID, songResult, artistResult, imageURL of the song to be removed

    first converts it into python dict
    then removes the song
    then converts it backs to the string

    retuns songs as string

    """
    new_songs = json.loads(songs)
    song = {
        "songID": songID,
        "songResult": songResult,
        "artistResult": artistResult,
        "imageURL": imageURL
    }

    new_songs.remove(song)
    songs = json.dumps(new_songs)

    return songs



def AddSharedUserByPlaylistCreator(playlists_shared_with, playlistID):
    """
    Takes the json string from user.playlists_shared_with
     playlistID -->  ID of the shared playlists of the user to be added

    first converts it into python dict
    then adds the  playlistID
    then converts it backs to the string

    retuns playlists_shared_with as string

    """
    print("In Database functions")

    add_playlists_shared_with = json.loads(playlists_shared_with)
    sharedPlaylist = {
        "playlistID": playlistID
    }
    print(sharedPlaylist)

    add_playlists_shared_with.append(sharedPlaylist)
    playlists_shared_with = json.dumps(add_playlists_shared_with)

    return playlists_shared_with
