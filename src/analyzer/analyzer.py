import csv, ast

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from scrapper.song import Song
from scrapper.scrapper import LIST_SONG_DIR

import plotly.plotly as py


def analyze_lyrics(lyrics):
    sid = SentimentIntensityAnalyzer()
    polarity = sid.polarity_scores(lyrics)

    return polarity


class Visualizer:

    songs_dict = {}

    def __init__(self):
        self.read_file()

    def read_file(self):
        songs = []

        with open(LIST_SONG_DIR, 'r') as csv_file:
            rows = csv.reader(csv_file, delimiter=',')

            for row in rows:
                s = Song(row[0], row[1], row[2], row[3])
                s.polarity = ast.literal_eval(row[4])

                songs.append(s)

        for song in songs:
            if song.polarity['compound'] == 0.0:
                continue

            if song.year not in self.songs_dict:
                self.songs_dict[song.year] = [song]
            else:
                self.songs_dict[song.year].append(song)

    def visualize(self):
        data = []
        for year, songs in self.songs_dict.items():
            data.append({
                'x': [song.rank for song in songs],
                'y': [song.polarity['compound'] for song in songs],
                'type': 'bar',
                'name': year})

        try:
            layout = {
                'xaxis': {'title': 'Rank'},
                'yaxis': {'title': 'Sentiments (pos / neg)'},
                'barmode': 'relative',
                'title': 'Hip Hop Lyrics Sentiment Analysis ({} - {})'.format
                (min(self.songs_dict.keys()), max(self.songs_dict.keys()))
            }

            py.iplot({'data': data, 'layout': layout}, filename='hip-hop-sentiment-analysis')
        except KeyError as err:
            print("Error:", err)
