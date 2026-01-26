# This file will randomly select 10 threads on DonWin for each of the control and upvote groups
from html.parser import HTMLParser

import requests
import time
from bs4 import BeautifulSoup as BSHTML
from datetime import datetime
import random
import os
import json
from urllib.parse import urlparse
import threading
import tenacity

# todo the big one, make it a rolling system so that upvotes can be applied as they come in for the moderate vote experiment
from tenacity import after_log
from urlextract import URLExtract

import logging
logging.basicConfig(filename='/tmp/votingExperiment.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

logger = logging.getLogger(__name__)

'''
method: scan the front page every minute and collect every thread that appears
note: make sure that threads already in a control or boosted group are removed
when finding a suitable thread, make sure that a suitable control thread is also selected


'''
controlGroup = []
boostedGroup = []
bothGroups = []

newThreadToMonitorDict = {}

baseFolder = "/home/dotty/donwinex/"
blandurls = {'v.redd.it', 'i.redd.it', 'reddit.com', 'youtube.com', 'video.maga.host', 'magaimg.net', 'i.maga.host',
             'i.imgur.com', 'youtu.be', 'twitter.com', 'mobile.twitter.com', 'imgur.com', 'm.youtube.com',
             'bitchute.com', 'instagram.com', 'giphy.com', 'media.thedonald.win', 'archive.maga.host', 'cdn.discordapp.com',
             'streamable.com', 'pbs.twimg.com', 'i.imgflip.com'}

donPostsDict = {}
jsonDictF = {}
extract = URLExtract()
with open('/run/media/dotty/Elements SE/Reddit3/BiasJson') as f:
    data_dict = json.load(f)

for x in data_dict:
    url = extract.find_urls(x)
    url = url[0].replace('www.', '')
    url = url.replace('amp.', '')
    name = x.split('(')[0]
    # print(url)
    jsonDictF[url] = [url, data_dict[x]]


class linkTracker:
    def __init__(self):
        self.totalposts = 0
        self.totalblandlinks = 0
        self.totaltrackednewslinks = 0
        self.totalselfposts = 0
        self.totaluntrackedposts = 0


class donaldPost:
    def __init__(self, postId, permalink, title, url):
        self.url = url
        self.postId = postId
        self.permalink = permalink
        self.title = title
        self.bias = -99


class trackedThread:
    def __init__(self):
        self.numberofgrabs = 0
        self.thread = None
        self.boosted = False


def incrementFolder(currentFolder):
    if os.path.isdir(baseFolder + "E" + "{:02d}".format(currentFolder)):
        currentFolder += 1
        return incrementFolder(currentFolder)
    else:
        os.mkdir(baseFolder + "E" + "{:02d}".format(currentFolder))
        currentDirectory = baseFolder + "E" + "{:02d}".format(currentFolder)
        return currentDirectory


@tenacity.retry(wait=tenacity.wait_fixed(30), after=after_log(logger, logging.ERROR))
def getfrontpage(numPages: int = 1):
    #if anything breaks, it's this <-
    donPostsDict = {}
    for i in range(1, numPages + 1):
        response = requests.get('https://thedonald.win/new', timeout=None)
        soup = BSHTML(response.text, 'html.parser')


        isError = soup.find('span', {"class": "cf-error-code"})
        while isError is not None:
            print("Connectivity error scraping front page!")
            time.sleep(10)
            response = requests.get('https://thedonald.win/new').text
            soup = BSHTML(response, 'html.parser')
            isError = soup.find('span', {"class": "cf-error-code"})

        donPosts = soup.find_all('div', {"class": "post"})
        postId = ''
        permalink = ''
        fullpermalink = ''
        title = ''
        url = ''
        assert len(donPosts) == 25
        for post in donPosts:
            postId = post.attrs["data-id"]
            author = post.attrs["data-author"]
            donSubPostTitle = post.findChildren('a', {"class": "title"}, recursive=True)
            assert len(donSubPostTitle) == 1
            for child in donSubPostTitle:
                title = str.strip(child.text)
                permalink = child.attrs['href']
                permalink1 = permalink.split('/')
                permalink2 = "/".join(permalink1[:3])
                permalink2 += "/"
                fullpermalink = 'https://thedonald.win' + permalink2
            donURL = post.findChildren('a', {"style": "display: initial"}, recursive=True)
            assert len(donURL) == 1
            url = donURL[0].attrs['href']
            donPostsDict[postId] = (donaldPost(postId, fullpermalink, title, url))
        if i > 1: time.sleep(3)
    return donPostsDict


def selectRollingThreadsWithBias():
    # Rolling bias vars
    suitableBoostedThreads = []
    suitableControlThreads = []
    blandthreads = []
    for thread in donPostsDict:
        linktracked.totalposts += 1
        urltemp = donPostsDict[thread].url
        urltemp = urlparse(urltemp)
        # urltemp[1] -> gets the host name from the url
        urltemp1 = urltemp[1]
        urltemp1 = urltemp1.replace('amp.', '')
        urltemp1 = urltemp1.replace('www.', '')
        if len(urltemp1) == 0:
            linktracked.totalselfposts += 1
            #suitableControlThreads.append(donPostsDict[thread])
        elif urltemp1 in blandurls:
            # print("Found a media link")
            linktracked.totalblandlinks += 1
            blandthreads.append(thread)
            #suitableControlThreads.append(donPostsDict[thread])
        elif urltemp1 in jsonDictF.keys():
            linktracked.totaltrackednewslinks += 1
            donPostsDict[thread].bias = jsonDictF[urltemp1]
            if donPostsDict[thread].bias[1] == -1 or donPostsDict[thread].bias[1] == 1 or donPostsDict[thread].bias[1] == 0:
                print("FOUND LOW BIAS URL: " + urltemp1)
                suitableBoostedThreads.append(donPostsDict[thread])
            else:
                print("found more extreme one with bias: " + str(donPostsDict[thread].bias[1]) + ", " + urltemp1)
                suitableControlThreads.append(donPostsDict[thread])
        else:
            print("Found MYSTERY LINK (good for control?): " + urltemp1)
            suitableControlThreads.append(donPostsDict[thread])
            linktracked.totaluntrackedposts += 1

    print("Processed the front page threads")
    return suitableControlThreads, suitableBoostedThreads


@tenacity.retry(wait=tenacity.wait_fixed(300), after=after_log(logger, logging.ERROR), stop=tenacity.stop_after_attempt(8))
def fiveMinScrape(currentfolder: str, trackedthread: trackedThread):
    proxyObj = dict(http='http://7cckc3ec2e5ac7j:7cckc3ec2e5ac7j@proxy.torguard.org:1337',
         https='https://7cckc3ec2e5ac7j:7cckc3ec2e5ac7j@proxy.torguard.org:1337')
    while trackedthread.numberofgrabs < 100:
        print("Tracking thread: " + trackedthread.thread.permalink + ", number of iters: " + str(
            trackedthread.numberofgrabs))
        isBoosted = trackedthread.boosted
        nowTime = datetime.now().strftime("%H:%M:%S")
        if not os.path.isdir(currentfolder + "/" + str(trackedthread.numberofgrabs)):
            try:
                os.mkdir(currentfolder + "/" + str(trackedthread.numberofgrabs))
            except:
                print("failed to make dir (warning)")
        nowFolder = currentfolder + "/" + str(trackedthread.numberofgrabs)
        controlFolder = nowFolder + "/" + "control"
        boostedFolder = nowFolder + "/" + "boosted"
        if not os.path.isdir(controlFolder):
            try:
                os.mkdir(controlFolder)
            except:
                print("failed to make dir (warning)")
        if not os.path.isdir(boostedFolder):
            try:
                os.mkdir(boostedFolder)
            except:
                print("failed to make dir (warning)")

        finalFolder = boostedFolder if isBoosted else controlFolder

        finalLink = trackedthread.thread.permalink.split("/")
        finalLink1 = finalLink[-2:-1][0]
        requestText = ""

        requestText = requests.get(trackedthread.thread.permalink, timeout=None, proxies=proxyObj).text

        #I indented this shit so maybe broke it :)
        soup = BSHTML(requestText, 'html.parser')

        isError = soup.find('span', {"class": "cf-error-code"})
        while isError is not None:
            time.sleep(60)
            print("Connectivity error scraping a thread")
            requestText = requests.get(trackedthread.thread.permalink, timeout=None, proxies=proxyObj).text
            soup = BSHTML(requestText, 'html.parser')
            isError = soup.find('span', {"class": "cf-error-code"})

        donScore = soup.find_all('span', {"class": "new-score"})
        assert len(donScore) == 1
        scoretotal = donScore[0].text
        scoreTemp1 = soup.find_all('span', {"class": "positive"})
        scoreTemp2 = soup.find_all('span', {"class": "negative"})
        assert len(scoreTemp1) > 0 and len(scoreTemp2) > 0, "No Pos / Neg scores found"
        scoreTemp3 = int(scoreTemp1[0].text)
        scoreTemp4 = int(scoreTemp2[0].text)

        commentCount = soup.find_all('div', {"class": "total"})
        assert len(commentCount) == 1
        commentCount1 = commentCount[0].contents[0]
        commentCount2 = commentCount1.strip()
        commentCount3 = commentCount2.replace("Comments (", "")
        commentCount4 = commentCount3.replace(")", "")

        with open(finalFolder + "/" + "totals" + ".txt", "a") as g:
            g.write(nowTime + "," + trackedthread.thread.permalink + "," + scoretotal + "," + str(
                scoreTemp3) + "," + str(scoreTemp4) + "," + commentCount4 + "\n")
            g.close()

        with open(finalFolder + "/" + finalLink1 + ".txt", "w") as f:
            f.write(requestText)
            f.close()

        trackedthread.numberofgrabs += 1
        rando = random.randint(0, 5)
        if trackedthread.numberofgrabs <= 12:
            time.sleep(296 + rando)
        elif trackedthread.numberofgrabs < 43:
            time.sleep(596 + rando)
        elif trackedthread.numberofgrabs < 97:
            time.sleep(1196 + rando)
        else:
            return 0
    return 0

if __name__ == "__main__":

    runCount = 0

    linktracked = linkTracker()
    nowTime = datetime.now().strftime("%H:%M:%S")
    currentFolder = incrementFolder(1)


    import sendafakevote

    # Do fake votes here
    sessionList = []

    for user in sendafakevote.users:
        session = sendafakevote.loginFunction(user)
        sessionList.append(session)

    sendafakevote.numVotestoApply = 10

    sendafakevote.voteDirection = 1

    assert len(
        sessionList) >= sendafakevote.numVotestoApply, "Not enough users available to apply this number of votes1"
    assert len(
        sendafakevote.users) >= sendafakevote.numVotestoApply, "Not enough users available to apply this number of votes2"

    if len(sendafakevote.users) > sendafakevote.numVotestoApply:
        sendafakevote.users = sendafakevote.users[:sendafakevote.numVotestoApply]
        sessionList = sessionList[:sendafakevote.numVotestoApply]

    threadpool = []
    continueRun = True

    globalMaxThreads = 100

    while continueRun:

        totalThreads = len(newThreadToMonitorDict.keys())

        if totalThreads < globalMaxThreads:
            donPostsDict = getfrontpage(1)
            suitableControlThreads, suitableBoostedThreads = selectRollingThreadsWithBias()
        else:
            print("Global max threads hit. Skipping /new. Time: " + datetime.now().strftime("%H:%M:%S"))

        numBoosted = 0 if len(newThreadToMonitorDict.keys()) == 0 else len(
            list(filter(lambda x: x.boosted, newThreadToMonitorDict.values())))

        for thread in suitableBoostedThreads:
            if thread.postId not in newThreadToMonitorDict.keys() and numBoosted < (globalMaxThreads/2):
                newtreadToMonitor = trackedThread()
                newtreadToMonitor.numberofgrabs = 0
                newtreadToMonitor.thread = thread
                newtreadToMonitor.boosted = True
                newThreadToMonitorDict[thread.postId] = newtreadToMonitor
                numBoosted += 1
                print("spawning thread (boosted) url:  " + thread.permalink)

                sendafakevote.urlToVote = thread.permalink
                for user, session in zip(sendafakevote.users, sessionList):
                    voteResponse = sendafakevote.applyVote(sendafakevote.urlToVote, session,
                                                           sendafakevote.voteDirection, user)
                    print("Got vote response: " + str(voteResponse))
                    assert voteResponse == 200, 'Voting failed! Sound the alarm'
                    time.sleep(2)
                print("Voting done!")
                print("Url Voted on: " + sendafakevote.urlToVote)
                print("Total users voted: " + str(sendafakevote.numVotestoApply))
                print("Vote direction: " + ("down" if sendafakevote.voteDirection == 0 else "up"))
                x = threading.Thread(target=fiveMinScrape, args=(currentFolder, newtreadToMonitor), daemon=True)
                threadpool.append(x)
                x.start()
            else:
                if numBoosted >= globalMaxThreads/2:
                    print("many boosted threads (max " + str(globalMaxThreads/2) + "): " + str(numBoosted))
                else:
                    print("thread already tracked (boosted)")
        suitableBoostedThreads = []

        numBoosted = 0 if len(newThreadToMonitorDict.keys()) == 0 else len(
            list(filter(lambda x: x.boosted, newThreadToMonitorDict.values())))
        numControl = len(newThreadToMonitorDict.values()) - numBoosted


        #check which threads are the newest
        haha1 = sorted(suitableControlThreads, key=lambda x: x.postId, reverse=True)
        for thread in haha1:
            if thread.postId not in newThreadToMonitorDict.keys() and numControl < numBoosted:
                numControl += 1
                newtreadToMonitor = trackedThread()
                newtreadToMonitor.numberofgrabs = 0
                newtreadToMonitor.thread = thread
                newtreadToMonitor.boosted = False
                newThreadToMonitorDict[thread.postId] = newtreadToMonitor
                print("spawning thread control " + thread.postId)
                x = threading.Thread(target=fiveMinScrape, args=(currentFolder, newtreadToMonitor), daemon=True)
                threadpool.append(x)
                x.start()
            else:
                if numControl >= numBoosted:
                    #print("too many control threads (>= Boosted)")
                    haha = ''
                else:
                    print("thread already tracked")
        suitableBoostedThreads = []

        print("Total number of active threads (threadpool): " + str(len(threadpool)))
        print("Total threads (thread.enumerate()): " + str(threading.activeCount()))

        if runCount > 120 and threading.activeCount() == 1:
            continueRun = False
        else:
            runCount += 1


        time.sleep(30)

        # frontpagethread = threading.Thread(target=threadGetfrontpage, args=(lock,), daemon=False)
    # frontpagethread.start()

    # selectRollingThreads = threading.Thread(target=selectRollingThreadsWithBias, args=(lock,), daemon=False)
    # selectRollingThreads.start()

    # suitableControlThreads, suitableBoostedThreads = selectRollingThreadsWithBias()

    print("ABSOLUTELY EVERYTHING FINISHED. UNTIL NEXT TIME")
    time.sleep(10)
    quit(0)

    with open(currentFolder + "/" + "newestThreads.txt", "w") as f:
        for item in donPostsDict:
            f.write(donPostsDict[item].permalink + "\n")
        f.close()

    with open(currentFolder + "/" + "controlthreads.txt", "w") as f:
        for item in controlGroup:
            f.write(item.permalink + "\n")
        f.close()

    with open(currentFolder + "/" + "boostedthreads.txt", "w") as f:
        for item in boostedGroup:
            f.write(item.permalink + "\n")
        f.close()

    fiveMinScrape(currentFolder)

    timesrun = 0
    for timesrun in range(0, 23):
        time.sleep(300 - time.time() % 300)
        fiveMinScrape(currentFolder)
        print("Scraping again. 5 minute intervals. Current time is: " + nowTime)

    for timesrun in range(0, 132):
        time.sleep(600 - time.time() % 600)
        fiveMinScrape(currentFolder)
        print("Scraping again. 10 minute intervals. Current time is: " + nowTime)

    print("All done scraping for 24 hours. Toodles")
    # < 288
