class Song:
    def __init__(self, author, name, yr, rank):
        self.author = author.title()
        self.name = name.title()
        self.year = yr
        self.rank = rank

        self.polarity = 0

    def __iter__(self):
        return iter([self.author, self.name, self.year, self.rank, self.polarity])

    def __str__(self):
        return "Author: %s, Name: %s, Year: %s, Rank: %s, Polarity: %s"\
               % (self.author, self.name, self.year, self.rank, self.polarity)

    def __repr__(self):
        return "Author: %s, Name: %s, Year: %s, Rank: %s, Polarity: %s"\
               % (self.author, self.name, self.year, self.rank, self.polarity)
