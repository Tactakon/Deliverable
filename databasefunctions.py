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



def AddSharedUserByPlaylistCreator(listeners_shared_to, sharedUserID):
    """
    Takes the json string from playlist.listeners_shared_to
    sharedUserID --> UserID of the shareduser of the playlist to be added

    first converts it into python dict
    then adds the sharedUserID
    then converts it backs to the string

    retuns listeners_shared_to as string

    """
    print("In Database functions")

    add_isteners_shared_to = json.loads(listeners_shared_to)
    sharedUser = {
        "sharedUserID": sharedUserID
    }
    print(sharedUser)

    add_isteners_shared_to.append(sharedUser)
    listeners_shared_to = json.dumps(add_isteners_shared_to)

    return listeners_shared_to
