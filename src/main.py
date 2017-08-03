from scrapper.scrapper import *
from analyzer.analyzer import *

if __name__ == '__main__':
    start = 2014
    end = 2016

    #
    try:
        for year in range(start, end + 1):
            print("Retrieving lyrics for %d" % year)
            ss = SongScraper(Lyrics(year).get_songs())
            ss.scrape(analyze_lyrics)

    except KeyboardInterrupt:
        print("[Interrupted] Exiting the program")