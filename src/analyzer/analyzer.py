import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def analyze_lyrics(lyrics):
    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(lyrics)
