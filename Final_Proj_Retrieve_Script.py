import json
import requests
import spotipy
import os
import sqlite3
import spotipy.util as util
import lyricsgenius
from spotipy.oauth2 import SpotifyClientCredentials
#import matplotlib

#grabbing the top spotify tracks from a user's spotify account 
#returning a list of tuples [(song, artist), (song, artist), and so on...]
def grab_spotify_top_tracks(username, scope,client_id, client_secret, redirect_uri):
    song_artist = []
    #token = util.prompt_for_user_token(username ='Ejandre',scope='user-top-read', client_id='3b54d53b0c474780af4fa86c0242364b',client_secret='42c07ded757a42d69d12beef09424504',redirect_uri='https://accounts.spotify.com/authorize')
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    if token:
        sp_obj = spotipy.Spotify(token)
        results = sp_obj.current_user_top_tracks(time_range='medium_term',limit = 100)
        for name in results['items']:
            song_artist.append((name['name'], name['artists'][0]['name'], name['album']['name']))
            if name['name'] == "Fallen Angel":
                song_artist.remove(("Fallen Angel","Frankie Valli","Jersey Boys: Music From The Motion Picture And Broadway Musical"))
    print(song_artist)
    return song_artist

#grabbing drake's top 100 tracks from spotify
#returning a list of typles [(song, artist, album), and so on...]
def grab_drake_top_100(username, client_id, client_secret):
    res = []
    client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    tracks = sp.user_playlist_tracks(user=username, playlist_id='5w99BzxT7OOCz2oEkKCReG', fields=None, limit=10, offset=0, market=None)
    for x in tracks['items']:
        res.append((x['track']['name'], 
                    x['track']['album']['artists'][0]['name'], 
                    x['track']['album']['name']))
    return res

def get_song_lyrics(song,artist):
    gen_obj = lyricsgenius.Genius("uwm7hKHlSCzTd6jsJVxKx0CGv_TumqMn-YK4Eh1WNBkwAEYz5tbWSU31iYfrQaOO")
    gen_obj.remove_section_headers = True
    gen_obj.skip_non_songs = True
    song = gen_obj.search_song(song, artist)
    lyrics = song.lyrics
    return lyrics

def write_lyrics_to_txt(lyrics,filename):
    f = open(filename, "a", encoding='utf8')
    f.write(lyrics)
    f.close()

def check_frequency_of_words(text):
    freq = {}
    read_txt = open(text, "r", encoding = 'utf8')
    for word in read_txt.readlines():
        word = word.lower()
        for w in word.split():
            if w not in freq:
                freq[w] = 1
            else:
                freq[w] += 1
    x = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return x[:100]

def setUpDatabase(db_name):                                
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn     

#creates a table for artist, song, album for user 
def add_user_tracks(tracks, cur, conn):
    tracks = grab_spotify_top_tracks('Shanley Corvite', 'user-top-read', '477f0c7f45be49758dd061c8c15176a1', 'a758f2131c0346e79e88383664260be0', 'https://accounts.spotify.com/authorize')
    conn = sqlite3.connect('MainDatabase.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS UserTracks (song TEXT, artist TEXT, album TEXT)")
    count = 0
    for tup in tracks:
        if count == 20:
            break
        hui = cur.execute("SELECT song, artist FROM UserTracks WHERE song = ? AND artist = ?", (tup[0], tup[1])).fetchone()
        if cur.execute("SELECT song, artist FROM UserTracks WHERE song = ? AND artist = ?", (tup[0], tup[1])).fetchone() == None:
            cur.execute("INSERT INTO UserTracks (song, artist, album) VALUES (?, ?, ?)", (tup[0], tup[1], tup[2]))
            count += 1
        conn.commit()


#creates a table for word, frequency for user
def add_user_lyrics(x, cur, conn):
    x = check_frequency_of_words('lyrics.txt')
    conn = sqlite3.connect('MainDatabase.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS UserLyrics (word TEXT UNIQUE PRIMARY KEY, frequency INTEGER)")
    cur.executemany("INSERT INTO UserLyrics (word, frequency) VALUES (?, ?)", x)
    #count = 0
    #for word in x:
    #    if count == 20:
        #    break
        #hui = cur.execute("SELECT word, frequency FROM UserLyrics WHERE word = ? and frequency = ?", (word[0], word[1])).fetchone()
        #if cur.execute("SELECT word, frequency FROM UserLyrics WHERE word = ? and frequency = ?", (word[0], word[1])).fetchone() == None:
        #    cur.execute("INSERT INTO UserLyrics(word, frequency) VALUES (?, ?)", (word[0], word[1]))
        #    count += 1
    conn.commit()


#creates a table for song, artist, album for drake
def add_drake_tracks(tracks, cur, conn):
    tracks = grab_drake_top_100('Shanley Corvite', '477f0c7f45be49758dd061c8c15176a1', 'a758f2131c0346e79e88383664260be0')    
    conn = sqlite3.connect('MainDatabase.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS DrakeTracks (song TEXT, drake TEXT, album TEXT)")
    count = 0
    for tup in tracks:
        if count == 20:
            break
        hui = cur.execute("SELECT song, drake FROM DrakeTracks WHERE song = ? AND drake = ?", (tup[0], tup[1])).fetchone()
        if cur.execute("SELECT song, drake FROM DrakeTracks WHERE song = ? AND drake = ?", (tup[0], tup[1])).fetchone() == None:
            cur.execute("INSERT INTO DrakeTracks (song, drake, album) VALUES (?, ?, ?)", (tup[0], tup[1], tup[2]))
            count+=1
        conn.commit()

#creates a table for word, frequency for drake 
def add_drake_lyrics(x, cur, conn):
    x = check_frequency_of_words('lyrics2.txt')
    conn = sqlite3.connect('MainDatabase.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS DrakeLyrics (word TEXT, frequency INTEGER)")
    cur.executemany("INSERT INTO DrakeLyrics (word, frequency) VALUES (?, ?)", x)
    conn.commit()


def main():
    #person1 = grab_spotify_top_tracks('Ejandre','user-top-read','3b54d53b0c474780af4fa86c0242364b','42c07ded757a42d69d12beef09424504','https://accounts.spotify.com/authorize')
    person1 = grab_spotify_top_tracks('Shanley Corvite', 'user-top-read', '477f0c7f45be49758dd061c8c15176a1', 'a758f2131c0346e79e88383664260be0', 'https://accounts.spotify.com/authorize')
    #drake_compare = grab_drake_top_100('Ejandre', '3b54d53b0c474780af4fa86c0242364b','42c07ded757a42d69d12beef09424504')
    drake_compare = grab_drake_top_100('Shanley Corvite', '477f0c7f45be49758dd061c8c15176a1','a758f2131c0346e79e88383664260be0')

    for x in person1:
        try:
            lyr = get_song_lyrics(x[0],x[1])
        except:
            continue

        write_lyrics_to_txt(lyr, "lyrics.txt")
    print(check_frequency_of_words("lyrics.txt"))

    for y in drake_compare:
        try:
            lyr2 = get_song_lyrics(y[0],y[1])
        except:
            continue
        write_lyrics_to_txt(lyr2,"lyrics2.txt")
    print(check_frequency_of_words("lyrics2.txt"))

    
    cur, conn = setUpDatabase('MainDatabase.db')
    
    data = grab_spotify_top_tracks('Shanley Corvite', 'user-top-read', '477f0c7f45be49758dd061c8c15176a1', 'a758f2131c0346e79e88383664260be0', 'https://accounts.spotify.com/authorize')
    add_user_tracks(data, cur, conn)
    add_user_lyrics(x, cur, conn)

    tracks = grab_drake_top_100('Shanley Corvite', '477f0c7f45be49758dd061c8c15176a1', 'a758f2131c0346e79e88383664260be0')    
    add_drake_tracks(tracks, cur, conn)
    add_drake_lyrics(x, cur, conn)
    conn.close()
   

if __name__ == "__main__":
    main()

