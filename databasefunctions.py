import json

"""
Takes the json string from playlist.songs
songID, songResult, artistResult of the song to be added

first converts it into python dict
then adds the song
then converts it backs to the string

retuns songs as string

"""
def AddSongtoPlaylist(songs, songID, songResult, artistResult):
    new_songs = json.loads(songs)
    song = {
        "songID": songID,
        "songResult": songResult,
        "artistResult": artistResult
    }

    new_songs.append(song)
    songs = json.dumps(new_songs)
    
    return songs

"""
Takes the json string from playlist.songs
songID, songResult, artistResult of the song to be removed

first converts it into python dict
then removes the song
then converts it backs to the string

retuns songs as string

"""
def RemoveSongFromPlaylist(songs, songID, songResult, artistResult):
    new_songs = json.loads(songs)
    song = {
        "songID": songID,
        "songResult": songResult,
        "artistResult": artistResult
    }

    new_songs.remove(song)
    songs = json.dumps(new_songs)

    return songs


"""
Takes the json string from playlist.listeners_shared_to
sharedUserID --> UserID of the shareduser of the playlist to be added

first converts it into python dict
then adds the sharedUserID
then converts it backs to the string

retuns listeners_shared_to as string

"""

def AddSharedUserByPlaylistCreator(listeners_shared_to, sharedUserID):
    print("In Database functions")

    add_isteners_shared_to = json.loads(listeners_shared_to)
    sharedUser = {
        "sharedUserID": sharedUserID
    }
    print(sharedUser)

    add_isteners_shared_to.append(sharedUser)
    print("listeners_shared_to: " )
    print(add_isteners_shared_to)
    listeners_shared_to = json.dumps(add_isteners_shared_to)

    return listeners_shared_to