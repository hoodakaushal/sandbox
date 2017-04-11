import csv
import pickle

class Entry:
    def __init__(self, name, author, votes, link):
        self.name = name
        self.author = author
        self.votes = int(votes)
        self.link = link

    def __cmp__(self, other):
        assert isinstance(other, Entry)
        if self.votes > other.votes:
            return -1
        elif self.votes < other.votes:
            return 1
        else:
          if self.author < other.author:
              return -1
          elif self.author > other.author:
              return 1
          else:
              if self.name < other.name:
                  return -1
              elif self.name > other.name:
                  return 1
              else:
                  return 0

    def __repr__(self):
        return "|[*" + self.name + "*](" + self.link + ")|" + self.author + "|" + str(self.votes)

def reader(path):
    with open(path,'rb') as sheet:
        reader = csv.reader(sheet, delimiter='\t')
        entries = []
        for row in reader:
            entries.append(Entry(row[0], row[1], row[2], row[3]))
        entries.sort()
        return entries

def poster(entries):
    preamble = """This list includes all those entries that got at least two votes. Books that received equal number of votes get the same rank. The links take you to the Goodreads page for the book.

You can see the full list on [this](https://docs.google.com/spreadsheets/d/1QBerJl-Nr60dS-N_YuEZ8mBHRowFHwGLHZtR3hAGzF4/edit?usp=sharing) google spreadsheet. And [here's](https://www.reddit.com/r/Fantasy/comments/5p3cl7/the_rfantasy_best_standalone_novels_poll/) the voting thread.

No.|Name|Author|Votes
--:|:--|:--|--:
"""
    r = ranks(entries)
    assert len(r) == len(entries)
    for i in range(len(entries)):
        if entries[i].votes > 1:
            preamble += str(r[i]) + str(entries[i]) + '\n'
    return preamble



def ranks(entries):
    ranks = [1]
    rank = 1
    buffer = 0
    for i in range(1, len(entries)):
        if entries[i].votes == entries[i-1].votes:
            buffer += 1
        else:
            rank = buffer + rank + 1
            buffer = 0
        ranks.append(rank)
    return ranks



def runner():
    f = "C:\\Users\\hooda\\Downloads\\rFantasy.tsv"
    entries = reader(f)
    post = poster(entries)
    print(post)

runner()
