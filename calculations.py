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
        print("Couldn't connect to Database")
    return conn

def get_freq(conn):
    freq_dict = {} 
    freq_list = []
    cur = conn.cursor()
    sum_word = cur.execute('SELECT SUM(frequency) FROM UserLyrics').fetchone()
    data_words = cur.execute('SELECT word, frequency FROM UserLyrics')
    for x in cur.fetchall():
        freq_list.append(x)
    for row in freq_list:
        freq = row[1] / sum_word[0]
        freq_dict[row[0]] = freq
    #print(freq_list)
    conn.commit()
    print(freq_dict)
    return freq_dict

def write_calc_to_text(data):
    f = open("calc_freq.txt", "w" , encoding = "utf-8")
    f.write(json.dumps(data))


'''
def pie_chart_top_artists(data):
    dict_data = json.loads(data)
    labels = dict_data.keys()
    sizes = dict_data.values()
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    fig.savefig("piechart.png")
'''

def bar_chart_word(data):
    dict_data = json.loads(data.read())
    labels = dict_data.keys()
    sizes = dict_data.values()
    plt.bar(labels,sizes, color='red')
    plt.show()
    plt.savefig("barchart.png")


connect = set_connection("MainDatabase.db")
write_calc_to_text(get_freq(connect))
bar_chart_word(open("calc_freq.txt"))