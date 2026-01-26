#This file takes in a ChompJSON and calculates basic stats (total comments, karma, etc., broken down by subreddit
import datetime
from itertools import islice

import json
from dateutil import tz

import glob


folderName = '/home/dotty/donaldwin2/'

subReds = ['The_Donald', 'DonWin','politics','Showerthoughts','Conservative']
directoryread = '/home/dotty/donaldwin2/chompy/'
fileRead = 'ChompJson.txt'
directorywrite = directoryread

ndict1 = {}

filesToGrab = glob.glob(directoryread + "*.txt")

#Key is String of Date + SubRed


#Dictionary of strings(dates) => Objects

'''
Heirachy is:
Subreddit
    |
    -> Dictionary of string(dates) => Object (BasicStats?)
                                        |
                                        -> BasicStats
'''


class BasicStats:

    def __init__(self):
        self.totalComments = 0
        self.totalKarma = 0
        self.totalSubmissions = 0
        self.twitterLink = 0
        self.imageLinks = 0
        self.urlLinks = 0
        self.youtubelinks = 0

    def addComments(self, amount):
        self.totalComments += int(amount)

    def addKarma(self, amount):
        self.totalKarma += int(amount)

    def addSubmission(self):
        self.totalSubmissions += 1

    def toString(self):
        string1 = "Total Comments: " + str(self.totalComments)
        string1 += "\nTotal Karma: " + str(self.totalKarma)
        string1 += "\nTotal Submissions: " + str(self.totalSubmissions)
        return string1



def safe_div(x,y):
    if y == 0:
        return 0
    return x / y

mode = 'monthly'

def main():
    for infile1 in filesToGrab:
        with open(infile1, 'rt') as infile:
            for x in iter(lambda: list(islice(infile, 1)), []):
                parsed_json = json.loads(x[0])
                subRed = parsed_json['s']
                if subRed in subReds:
                    url = ''
                    title = parsed_json['t']
                    text = parsed_json['x']
                    url = parsed_json['u']
                    created = int(parsed_json['d'])
                    numComments = str(parsed_json['c'])
                    numComments = str.replace(numComments,'comment','')
                    dt = datetime.datetime.fromtimestamp(created, tz=tz.UTC)
                    karma = parsed_json['k']
                    strDate = str(dt.date())
                    strMonth = strDate[:-3]
                    if mode == 'daily':
                        createdString = subRed + strDate
                    elif mode == 'monthly':
                        createdString = subRed + strMonth
                    else:
                        assert 0
                    if(createdString not in ndict1):
                        print("didn't find LOL!")
                        ndict1[createdString] = BasicStats()
                    ndict1[createdString].addKarma(karma)
                    ndict1[createdString].addComments(numComments)
                    ndict1[createdString].addSubmission()


if __name__ == "__main__":
    main()
    nlist1 = ndict1.items()
    for item in sorted(nlist1):
        print(item[0])
        print(item[1].toString())

