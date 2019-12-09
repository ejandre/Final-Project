import json
import requests
import spotipy
import os
import sqlite3
import spotipy.util as util
import lyricsgenius

def grab_spotify_top_tracks(username,scope,client_id,client_secret,redirect_uri):
    song_artist = []
    #token = util.prompt_for_user_token(username ='Ejandre',scope='user-top-read', client_id='3b54d53b0c474780af4fa86c0242364b',client_secret='42c07ded757a42d69d12beef09424504',redirect_uri='https://accounts.spotify.com/authorize')
    token = util.prompt_for_user_token(username,scope, client_id,client_secret,redirect_uri)
    if token:
        sp_obj = spotipy.Spotify(token)
        results = sp_obj.current_user_top_tracks(time_range='medium_term',limit = 20)
        for name in results['items']:
            song_artist.append((name['name'], name['artists'][0]['name']))
            if name['name'] == "Fallen Angel":
                song_artist.remove(("Fallen Angel","Frankie Valli"))
    print(song_artist)
    return song_artist


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
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)

    


def main():
    person1 = grab_spotify_top_tracks('Ejandre','user-top-read','3b54d53b0c474780af4fa86c0242364b','42c07ded757a42d69d12beef09424504','https://accounts.spotify.com/authorize')
    person2 = grab_spotify_top_tracks('Shanley Corvite','user-top-read','477f0c7f45be49758dd061c8c15176a1','a758f2131c0346e79e88383664260be0','https://accounts.spotify.com/authorize')
    for x in person1:
        try:
            lyr = get_song_lyrics(x[0],x[1])
        except:
            continue

        write_lyrics_to_txt(lyr, "lyrics.txt")
    print(check_frequency_of_words("lyrics.txt"))

    for y in person2:
        try:
            lyr2 = get_song_lyrics(y[0],y[1])
        except:
            continue
        write_lyrics_to_txt(lyr2, "lyrics2.txt")

    print(check_frequency_of_words("lyrics2.txt"))


if __name__ == "__main__":
    main()

