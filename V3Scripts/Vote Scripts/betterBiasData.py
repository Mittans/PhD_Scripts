import json
import io
import re
from urlextract import URLExtract
from itertools import islice
from collections import defaultdict
from urllib.parse import urlparse
from datetime import datetime
import operator
import pytz
import os


tz = pytz.timezone('UTC')

totalcount = 0
totalfound = 0
totalnotfound = 0
totalbland = 0
totalnolink = 0

extractor = URLExtract()
jsonDictF = {}
#files1 = ['RS_2018-09', 'RS_2018-10', 'RS_2018-11', 'RS_2018-12', 'RS_2019-01', 'RS_2019-02', 'RS_2019-03']
directoryread = '/home/dotty/donaldwin2/chompy/'
directorywrite = '/run/media/dotty/Elements SE/Reddit3/'
subReds = ['The_Donald', 'politics', 'Conservative', 'DonWin']
mode2 = 'daily' #daily #hourly
files1 = os.listdir('/home/dotty/donaldwin2/chompy/')
total1neg = 0
total1pos = 0
total1neutral =0
total1count = 0
blandurls = { 'v.redd.it', 'i.redd.it', 'reddit.com', 'youtube.com', 'magaimg.net', 'i.imgur.com', 'youtu.be', 'twitter.com', 'mobile.twitter.com', 'imgur.com', 'm.youtube.com', 'bitchute.com', 'instagram.com', 'giphy.com', 'media.thedonald.win',
              'streamable.com'}

ndict2 = {}

class biasObj:
    def __init__(self):
        self.name = "Neut"
        self.count = 0
        self.karma = 0
        self.totalStrength = 0

    def returnStrength(self):
        return self.totalStrength

    def addRecord(self, karma):
        self.count += 1
        self.karma += karma
        self.totalStrength += -999
        #Pos1
        #Count was 2
        #Karma was 10

        #Neg 1
        #Count is 1
        #Karma is 50

        #Pos 2
        #Karma is 20
        '''
        Total strength is 10
        '' is 50
        
        karma * 1*pos1 + karma * 2*pos2
        
        
        '''

class BasicStats:

#TheDon_Daily -> -4, -2, -1, 0, +1, +2, +4 bias objects
#Monthly = sum of all daily objects

    def __init__(self):
        self.totalComments = 0
        self.date = datetime.now()
