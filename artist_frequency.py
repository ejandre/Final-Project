import json
import requests
import spotipy
import os
import sqlite3
import spotipy.util as util
import lyricsgenius
from spotipy.oauth2 import SpotifyClientCredentials
#import matplotlib.pyplot as plt

def set_connection(db_file):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+db_file)
    except:
        print("Couldn't connect to database")
    return conn

def artist_frequency(conn):
    artist_dict = {}
    cur = conn.cursor()
    artists = cur.execute('SELECT artist FROM UserTracks').fetchall()
    for artist in artists:
        artist_0 = artist[0]
        if artist_0 not in artist_dict:
            artist_dict[artist_0] = 0
        artist_dict[artist_0]+= 1
    print(artist_dict)
    return artist_dict

def artist_text_file(artists):
    f = open('artist_frequency.txt', "w", encoding = 'utf-8')
    f.write(json.dumps(artists))

connect = set_connection("MainDatabase.db")
artist_text_file(artist_frequency(connect))