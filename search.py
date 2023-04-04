"""
This module contains functions for searching songs on Spotify.

Functions:
- search_song: search for songs on Spotify and return their names, artists, and ID
- parse_results: takes json file generated from API call in search_song function 
  and returns a tuple which contains 3 lists - songs, artists,ids and imageURLS
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# pylint: disable=unused-import
import requests
from dotenv import find_dotenv, load_dotenv
# pip3 install python-dotenv

load_dotenv(find_dotenv())
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
#must have variables named SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in a .env file

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                           client_secret=SPOTIPY_CLIENT_SECRET))
def search_song(query):
    """
    Search for songs on Spotify and return their names, artists,IDs and image URLs.

    Input:
    - query: the search query for the song

    Output:
    - songs: a list of the names of the matching songs
    - artists: a list of the names of the artists of the matching songs
    - ids: a list of the IDs of the matching songs
    - image_urls: a list of image URLS for matching songs
    """
    data = sp.search(q=query, limit=3)
    results = parse_results(data)
    return results
# pylint: disable=missing-function-docstring
def parse_results(data):
    songs = []
    artists = []
    ids = []
    image_urls = []
    # pylint: disable=unused-variable
    for idx, track in enumerate(data['tracks']['items']):
        songs.append(track['name'])
        artists.append(track['artists'][0]['name'])
        ids.append(track['id'])
        image_urls.append(track['album']['images'][0]['url'])
    return songs, artists, ids, image_urls
