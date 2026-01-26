#This file parses html files scraped from TheDonald.Win and turns them into a ChompJSON suitable for use
#By the other Reddit scraping tools



from html.parser import HTMLParser
import io
from bs4 import BeautifulSoup as BSHTML
from datetime import datetime
import pytz
import json

folderName = '/home/dotty/donaldwin2/'
fileName = 'index'
indexStart = 1
indexMax = 8317

threadIdDict = {}

postId = ''
author = ''
title = ''
text = ''
url = ''
permalink = ''
karma = ''
numComments = ''
flair = ''
subRed = 'DonWin'
text = ''
created = ''

f = open(folderName + 'ChompJson3.txt', 'wt+')


for i in range(indexStart,indexMax):
    fileOpen2 = open(folderName + fileName + str(i), 'r')
    soup = BSHTML(fileOpen2.read(), 'html.parser')
    donPosts = soup.find_all('div', {"class": "post"})
    assert len(donPosts) == 25
    for post in donPosts:
        postId = text = post.attrs["data-id"]
        author = post.attrs["data-author"]

        donFlair = post.findChildren('span', {"class": "post-flair"}, recursive=True)
        assert len(donFlair) <= 1
        if len(donFlair) == 0: flair = 'null'
        else: flair = donFlair[0].attrs['data-flair']

        donComments = post.findChildren('a', {"class": "original comments"}, recursive=True)
        assert len(donComments) == 1
        numComments = str.replace(donComments[0].text, " comments", "")

        donKarma = post.findChildren('span', {"class": "count"}, recursive=True)
        assert len(donKarma) == 1
        karma = donKarma[0].text

        donSubPostTitle = post.findChildren('a', {"class": "title"}, recursive=True)
        assert len(donSubPostTitle) == 1
        for child in donSubPostTitle:
            title = str.strip(child.text)
            permalink = child.attrs['href']

        donURL = post.findChildren('a', {"style": "display: initial"}, recursive=True)
        assert len(donURL) == 1
        url = donURL[0].attrs['href']

        donCreatedTime = post.findChildren('time', {"class": "timeago"}, recursive=True)
        assert len(donCreatedTime) == 1
        datetime1 = donCreatedTime[0].attrs["datetime"]
        test123 = datetime1[:-1]
        datetime2 = datetime.fromisoformat(datetime1[:-1])
        datetime3 = datetime2.replace(tzinfo=pytz.timezone('US/Eastern'))
        created = str(int(datetime3.timestamp()))

        dict1 = {}
        dict1['s'] = subRed
        dict1['a'] = author
        dict1['t'] = title
        dict1['x'] = text
        dict1['p'] = permalink
        dict1['f'] = flair
        dict1['d'] = created
        dict1['u'] = url
        dict1['c'] = numComments
        dict1['k'] = karma
        threadIdDict[postId] = dict1

for item in threadIdDict:
    item1 = json.dumps(threadIdDict[item], separators=(',', ':'))
    f.write(item1 + "\n")
f.close()




#ThreadID, Author = <div class="post  mobile_guest" data-type="post" data-id="557308" data-author="BasementBiden">
#Upvote count = <span class="count">11</span>

#PermaLink = <a href="/p/GbyHwyoi/cant-sleep-because-too-much-maga/" class="title">
    #CAN&#39;T SLEEP BECAUSE TOO MUCH MAGA ENERGY SO I CRUSHED A WORKOUT AT 1 IN THE MORNING! I CAN&#39;T WAIT FOR NOVEMBER! LET&#39;S FUCKING GOOOOOOO!!!
#</a>

#PostFlair = <span class="post-flair" data-flair="fire">&#x1f525; FIRE & FURY &#x1F4A5;</span>

#DateTime = <span class="since">posted <time class="timeago" datetime="2020-08-05T05:51:13Z" title="Wed Aug 05 01:51:13 EDT 2020">21 minutes</time> ago by <a href="/u/BasementBiden/" class="author">BasementBiden</a></span>

'''
                    dict1['s'] = subRed
                    dict1['a'] = author
                    dict1['t'] = title
                    dict1['x'] = text
                    dict1['p'] = permalink
                    dict1['f'] = flair
                    dict1['d'] = created
                    dict1['u'] = url
                    dict1['c'] = numComments
                    dict1['k'] = karma
'''

