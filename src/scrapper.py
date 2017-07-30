import os
import urllib2
import csv

from bs4 import BeautifulSoup

CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
LIST_SONG_DIR = "list-songs.csv"
BILLBOARD_TOP_HITS = "http://www.billboard.com/charts/year-end/%s/hot-r-and-and-b-hip-hop-songs"


class Song:
    def __init__(self, author, name, year, rank):
        self.author = author
        self.name = name
        self.year = year
        self.rank = rank


# Get url page content
def get_page(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    return response.read()


# Get list of top songs from billboard top chart
class Lyrics:
    link = ""

    def __init__(self, year):
        self.year = year
        self.link = BILLBOARD_TOP_HITS % year

    # Return a list of songs
    def get_songs(self):
        page = get_page(self.link)
        soup = BeautifulSoup(page, "html.parser")
        soup = soup.get_text()

        # print soup
        return [Song("Stan", "Name", 1991, 1)]


# Scrape song from site
class SongScraper:
    def __init__(self, songs):
        self.songs = songs

    def scrape(self):
        for song in self.songs:
            self.ScrapeSongLyrics(song)

        self.update_song_list()

    def update_song_list(self):
        with open(LIST_SONG_DIR, 'a') as f:
            writer = csv.writer(f,
                                delimiter=',',
                                lineterminator='\n',
                                quoting=csv.QUOTE_ALL)

            for song in self.songs:
                writer.writerow(vars(song).values())

    class ScrapeSongLyrics:
        link = ""
        content = ""
        dir_path = ""

        def __init__(self, song):
            self.song = song

            self.dir_path = "%s/%d" % (CACHE_DIR, song.year)
            self.create_dir()
            self.find_lyrics_link()
            self.get_lyrics()
            self.save_lyrics()

        def find_lyrics_link(self):
            pass

        def get_lyrics(self):
            page = get_page(self.link)

        def save_lyrics(self):
            pass

        def create_dir(self):
            if not os.path.isdir(self.dir_path):
                os.makedirs(self.dir_path)


if __name__ == '__main__':
    start = 2015
    end = 2017

    for year in range(start, end):
        SongScraper(Lyrics(year).get_songs()).scrape()
