import os
from pathlib import Path
import csv
import operator
from datetime import datetime as dt
from dateutil import parser
import  pickle
import copy
import pandas as pd

class episodeClass:
    def __init__(self):
        self.episode = ''
        self.score = 0
        self.comments = 0
        self.group = ''
        self.timeseries = 0
        self.time = dt.today()

completedFolders = '/home/dotty/donwinex/Good/'

subfolders = [ f.path for f in os.scandir(completedFolders) if f.is_dir() ]

episodeList = []

test1df = pd.DataFrame(None, columns=['Score', 'Comments', 'Group', 'TimeSeries','TimeIndex'])
fivemins = pd.timedelta_range(0, periods=13, freq='5T')
tenmins = pd.timedelta_range('1H10T', periods=30, freq='10T')
fifteenmins = pd.timedelta_range('6H20T', periods=54, freq='20T')
totalmins = fivemins.append(tenmins).append(fifteenmins)


for x in subfolders:
    episode = x.split("/")[-1:][0]
    episode1 = episodeClass()
    episode1.episode = episode
    paths = sorted(Path(x).iterdir(), key=os.path.getmtime)
    paths = list(filter(lambda y: Path(y).is_dir(), paths))
    episode1.timeSeriesLength = len(paths)
    i = 0
    for y in paths:
        totalsControlFile = open(str(y) + "/control/totals.txt", "r")
        totalsBoostedFile = open(str(y) + "/boosted/totals.txt", "r")
        j = 0
        for line in totalsBoostedFile:
            line1 = line.split(',')
            boostedComments = int(line1[5])
            boostedScore = int(line1[2])
            episode1.score = boostedScore
            episode1.comments = boostedComments
            episode1.timeseries = i
            time123 = parser.parse(line1[0])
            episode1.time = time123
            episode1.group = "Boosted"
            #episodeList.append(copy.copy(episode1))

            episode = episode1.episode
            score = episode1.score
            comments = episode1.comments
            group = episode1.group
            timeseries = episode1.timeseries
            time = totalmins[timeseries]
            test2 = pd.DataFrame([[score, comments, group, timeseries, time]],
                                 columns=['Score', 'Comments', 'Group', 'TimeSeries', 'TimeIndex'])
            test1df = test1df.append(test2, ignore_index=True)
            j+=1

        for line in totalsControlFile:
            line1 = line.split(',')
            controlComments = int(line1[5])
            controlScore = int(line1[2])
            episode1.score = controlScore
            episode1.comments = controlComments
            episode1.timeseries = i
            time123 = parser.parse(line1[0])
            episode1.time = time123
            episode1.group = "Control"
            #episodeList.append(copy.copy(episode1))

            episode = episode1.episode
            score = episode1.score
            comments = episode1.comments
            group = episode1.group
            timeseries = episode1.timeseries
            time = totalmins[timeseries]
            test2 = pd.DataFrame([[score, comments, group, timeseries, time]],
                                 columns=['Score', 'Comments', 'Group', 'TimeSeries', 'TimeIndex'])
            test1df = test1df.append(test2, ignore_index=True)
            j+=1
        i += 1

episodelist1 = episodeList


#test1df.reindex()
episodelist2 = open("timeseriesPickle1.pickle", "wb")
pickle.dump(test1df, episodelist2)
episodelist2.close()
quit(0)


for x in episodelist1:
    episode = x.episode
    score = x.score
    comments = x.comments
    group = x.group
    timeseries = x.timeseries
    time = totalmins[timeseries]
    test2 = pd.DataFrame([[score, comments, group, timeseries, time]], columns=['Score', 'Comments', 'Group', 'TimeSeries','TimeIndex'])
    test1df = test1df.append(test2)

episodelist2 = open("timeseriesPickle.pickle", "wb")
pickle.dump(test1df, episodelist2)
episodelist2.close()