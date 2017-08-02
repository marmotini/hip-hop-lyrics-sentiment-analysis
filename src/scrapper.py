#!/usr/bin/env python3

import os
import urllib.request, urllib.parse, urllib.error
import csv
import re
import time
import http.client

from bs4 import BeautifulSoup

CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
LIST_SONG_DIR = "list-songs.csv"
BILLBOARD_TOP_HITS = "http://www.billboard.com/charts/year-end/%s/hot-r-and-and-b-hip-hop-songs"
BILLBOARD_ANNUAL_MAX = 25
LYRICS_SEARCH_URL = "http://search.azlyrics.com/search.php?q=%s&w=songs&p=%d"


class Song:
    def __init__(self, author, name, yr, rank):
        self.author = author.title()
        self.name = name.title()
        self.year = yr
        self.rank = rank

    def __str__(self):
        return "Author: %s, Name: %s, Year: %s, Rank: %s" % (self.author, self.name, self.year, self.rank)


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def write_text_file(file_name, data, perm):
        with open(file_name, perm) as text_file:
            text_file.write("%s" % data)

    @staticmethod
    def create_dir(dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    # Get url page content
    @staticmethod
    def get_page(url):
        if url is None or url.strip() is "":
            return

        time.sleep(1)

        hdr = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
            'content-type': "application/json",
        }

        req = urllib.request.Request(url, headers=hdr)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.read()
        except urllib.error.HTTPError as err:
            print("HTTPError: Url %s Error %s" % (url, err))
        except http.client.BadStatusLine as err:
            print("BadStatusLine: Url %s Error %s. " % (url, err))

        return None


# Get list of top songs from billboard top chart
class Lyrics:
    link = ""

    def __init__(self, yr):
        self.year = yr
        self.link = BILLBOARD_TOP_HITS % year

        Helper.create_dir("%s/%d" % (CACHE_DIR, self.year))

    def gen_link_from_name(self):
        return "%s/%d/%s" % (CACHE_DIR, self.year, self.link.split('/')[-1])

    # Return a list of songs
    def get_songs(self):
        page = Helper.get_page(self.link)
        if page is None:
            return

        songs = []
        soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
        for s in soup.find_all(attrs={"class": "ye-chart__item-text"}):
            if len(songs) >= BILLBOARD_ANNUAL_MAX:
                break

            songs.append(Song(
                rank=s.find(attrs={"class": "ye-chart__item-rank"}).get_text().strip(),
                name=s.find(attrs={"class": "ye-chart__item-title"}).get_text().strip(),
                author=s.find(attrs={"class": "ye-chart__item-subtitle-link"}).get_text().strip(),
                yr=self.year))

        Helper.write_text_file("%s.html" % self.gen_link_from_name(), soup.prettify(), 'w+')

        return songs


# Scrape song from site
class SongScraper:
    def __init__(self, songs):
        if songs is None:
            self.songs = []
        else:
            self.songs = songs

    def scrape(self):
        for song in self.songs:
            self.ScrapeSongLyrics(song)

        self.update_song_list()

    def update_song_list(self):
        with open(LIST_SONG_DIR, 'a+') as f:
            writer = csv.writer(f,
                                delimiter=',',
                                lineterminator='\n',
                                quoting=csv.QUOTE_ALL)

            for song in self.songs:
                writer.writerow(list(vars(song).values()))

    class ScrapeSongLyrics:
        link = ""
        content = ""
        dir_path = ""
        max_pages_scrape = 7

        def __init__(self, song):
            self.song = song

            self.dir_path = "%s/%d" % (CACHE_DIR, song.year)

            self.find_lyrics_link()
            self.get_lyrics()
            self.save_lyrics()

        def find_lyrics_link(self, pages_count=1):
            page = Helper.get_page(LYRICS_SEARCH_URL % (self.song.name, pages_count))
            if page is None:
                return

            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")

            counts = soup.findAll(attrs={"class": "btn btn-share btn-nav"})
            if len(counts) > 1:
                temp = int(counts[-2].get_text().strip())
                if temp < self.max_pages_scrape:
                    self.max_pages_scrape = temp

            for song in soup.find_all(attrs={"class": "visitedlyr"}):
                for s1 in song.findAll("b", text=self.song.name):
                    author = s1.parent.parent.find(text=re.compile(r'' + self.song.author.split(' ', 1)[0] + ''))
                    if author is not None:
                        self.link = s1.parent.parent.find('a', href=True)["href"]
                        return

            pages_count += 1

            if pages_count >= self.max_pages_scrape:
                return

            self.find_lyrics_link(pages_count)

        def get_lyrics(self):
            print("%s %s lyrics. Link: %s" % (self.song.author, self.song.name, self.link))
            page = Helper.get_page(self.link)
            if page is None:
                return

            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            t = soup.prettify()
            t = t.split("<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->", 1)[-1]
            t = t.split("<!-- MxM banner -->", 1)[0]

            t1 = t.replace('<br/>', '').replace('<i>', '').replace('</i>', '').replace('</div>', '')
            t3 = t1.split('\n')

            t4 = '\n'.join([line.strip() for line in t3 if line.strip() != ""])
            t4 = self.consume_paren(t4)

            Helper.write_text_file("%s/%s-%s.txt" %
                                   (self.dir_path, self.song.name.replace("/", "-"), self.song.author), t4, 'w+')

        def consume_paren(self, text):
            ret = ''
            skip1c = 0
            skip2c = 0
            for i in text:
                if i == '[':
                    skip1c += 1
                elif i == '(':
                    skip2c += 1
                elif i == ']' and skip1c > 0:
                    skip1c -= 1
                elif i == ')' and skip2c > 0:
                    skip2c -= 1
                elif skip1c == 0 and skip2c == 0:
                    ret += i
            return ret

        def save_lyrics(self):
            pass


if __name__ == '__main__':
    start = 2014
    end = 2016

    try:
        for year in range(start, end + 1):
            print("Retrieving lyrics for %d" % year)
            SongScraper(Lyrics(year).get_songs()).scrape()
    except KeyboardInterrupt:
        print("[Interrupted] Exiting the program")
