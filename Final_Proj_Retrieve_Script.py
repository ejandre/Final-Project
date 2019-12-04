import json
import requests
import csv
import spotipy
import os
import sqlite3
import spotipy.util as util
from bs4 import BeautifulSoup

def grab_spotify_top_tracks(username,scope,client_id,client_secret,redirect_uri):
    song_artist = {}
    #token = util.prompt_for_user_token(username ='Ejandre',scope='user-top-read', client_id='3b54d53b0c474780af4fa86c0242364b',client_secret='42c07ded757a42d69d12beef09424504',redirect_uri='https://accounts.spotify.com/authorize')
    token = util.prompt_for_user_token(username,scope, client_id,client_secret,redirect_uri)
    if token:
        sp_obj = spotipy.Spotify(token)
        results = sp_obj.current_user_top_tracks(time_range='medium_term',limit = 20)
        for name in results['items']:
            song_artist[name['name']] = name['artists'][0]['name']
        print(song_artist)
    return song_artist


eric = grab_spotify_top_tracks('Ejandre','user-top-read','3b54d53b0c474780af4fa86c0242364b','42c07ded757a42d69d12beef09424504','https://accounts.spotify.com/authorize')
#shanley =  grab_spotify_top_tracks('','','','','https://accounts.spotify.com/authorize')



def get_song_info():
    pass
