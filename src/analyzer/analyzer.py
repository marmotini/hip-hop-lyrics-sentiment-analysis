from nltk.sentiment.vader import SentimentIntensityAnalyzer

v = None


def analyze_lyrics(lyrics, song):
    sid = SentimentIntensityAnalyzer()
    polarity = sid.polarity_scores(lyrics)

    global v

    if v is None:
        v = Visualizer()

    v.visualize(polarity, song)

    return polarity


class Visualizer:
    def __init__(self):
        pass

    def visualize(self, polarity, song):
        print("Polarity: {0}, Song: {1}".format(polarity, song))

        pass
