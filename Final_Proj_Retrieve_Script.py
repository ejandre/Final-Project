import json
import requests
import csv
import spotipy
import os
import sqlite3
import spotipy.util as util
from bs4 import BeautifulSoup

def grab_spotify_top_tracks():
    token = util.prompt_for_user_token(username ='Ejandre',scope='user-top-read', client_id='3b54d53b0c474780af4fa86c0242364b',client_secret='42c07ded757a42d69d12beef09424504',redirect_uri='https://accounts.spotify.com/authorize')
    if token:
        sp_obj = spotipy.Spotify()
        results = sp_obj.current_user_top_tracks(time_range='medium_term',limit = 20)
        print(results)


grab_spotify_top_tracks()




def get_song_info():
    pass
