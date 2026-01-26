#This file will randomly select 10 threads on DonWin for each of the control and upvote groups
from html.parser import HTMLParser

import requests
import time
from bs4 import BeautifulSoup as BSHTML
from datetime import datetime
import random
import os

'''
method: scan the front page every minute and collect every thread that appears
note: make sure that threads already in a control or boosted group are removed
when finding a suitable thread, make sure that a suitable control thread is also selected



'''
controlGroup = []
boostedGroup = []
bothGroups = []

baseFolder = "/home/dotty/donwinex/"


donPostsDict = {}

class donaldPost:
    def __init__(self, postId, permalink, title, url):
        self.url = url
        self.postId = postId
        self.permalink = permalink
        self.title = title

def incrementFolder(currentFolder):
    if os.path.isdir(baseFolder + "E" + "{:02d}".format(currentFolder)):
        currentFolder += 1
        return incrementFolder(currentFolder)
    else:
        os.mkdir(baseFolder + "E" + "{:02d}".format(currentFolder))
        currentDirectory = baseFolder + "E" + "{:02d}".format(currentFolder)
        return currentDirectory



def getfrontpage(numPages: int=1):
    for i in range(1,numPages+1):
        response = requests.get('https://thedonald.win/search?sort=new&params=&page=' + str(i))
        soup = BSHTML(response.text, 'html.parser')
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

def selectXthreadsNewest(amountPerGroup=10, mode='random'):
    #available modes are 'random', 'biasmild', 'biasstrong', 'biaseither'
    if mode == 'random':
        listDic = list(donPostsDict.values())
        random.shuffle(listDic)
        controlGroup = listDic[:amountPerGroup]
        boostedGroup = listDic[amountPerGroup:2*amountPerGroup]
        assert len(controlGroup) == amountPerGroup and len(boostedGroup) == amountPerGroup, "Not enough threads to divide into control group or boosted group! Exploding"
        for item in boostedGroup:
            assert not any(x.permalink == item.permalink for x in controlGroup), "Found boosted url in control group urls. That's bad"
    elif mode == 'biasmild':
        #todo select threads by bias :)
        print("todo")
    else:
        assert False, "Unhandled select mode! Exploding"

    return controlGroup, boostedGroup

def runExperimentfor24hours():
    return 0


def collectThreadStats(threadUrl: str):
    response = requests.get(threadUrl)



def fiveMinScrape(currentfolder: str):
    nowTime = datetime.now().strftime("%H:%M:%S")
    os.mkdir(currentfolder + "/" + nowTime)
    nowFolder = currentfolder + "/" + nowTime
    controlFolder = nowFolder + "/" + "control"
    boostedFolder = nowFolder + "/" + "boosted"
    os.mkdir(controlFolder)
    os.mkdir(boostedFolder)
    for item in controlGroup:
        scoretotal = 0
        scorenegative = 0
        scorepositive = 0
        finalLink = item.permalink.split("/")
        finalLink1 = finalLink[-2:-1][0]
        requestText = ""
        with open(controlFolder + "/" + finalLink1 + ".txt", "w") as f:
            requestText = requests.get(item.permalink).text
            f.write(requestText)
            f.close()
            soup = BSHTML(requestText, 'html.parser')
            donScore = soup.find_all('span', {"class": "new-score"})
            assert len(donScore) == 1
            scoretotal = donScore[0].text
            scoreTemp1 = soup.find_all('span', {"class": "positive"})
            scoreTemp2 = soup.find_all('span', {"class": "negative"})
            assert len(scoreTemp1) > 0 and len(scoreTemp2) > 0, "No Pos / Neg scores found"
            scoreTemp3 = int(scoreTemp1[0].text)
            scoreTemp4 = int(scoreTemp2[0].text)

            commentCount = soup.find_all('div', {"class":"total"})
            assert len(commentCount) == 1
            commentCount1 = commentCount[0].contents[0]
            commentCount2 = commentCount1.strip()
            commentCount3 = commentCount2.replace("Comments (", "")
            commentCount4 = commentCount3.replace(")", "")


            with open(controlFolder + "/" + "totals" + ".txt", "a") as g:
                g.write(nowTime + "," + item.permalink + "," + scoretotal + "," + str(scoreTemp3) + "," + str(scoreTemp4) + "," + commentCount4 + "\n")
                g.close()

    for item in boostedGroup:
        scoretotal = 0
        scorenegative = 0
        scorepositive = 0
        finalLink = item.permalink.split("/")
        finalLink1 = finalLink[-2:-1][0]
        requestText = ""
        with open(boostedFolder + "/" + finalLink1 + ".txt", "w") as f:
            requestText = requests.get(item.permalink).text
            f.write(requestText)
            f.close()
            soup = BSHTML(requestText, 'html.parser')
            donScore = soup.find_all('span', {"class": "new-score"})
            assert len(donScore) == 1
            scoretotal = donScore[0].text
            scoreTemp1 = soup.find_all('span', {"class": "positive"})
            scoreTemp2 = soup.find_all('span', {"class": "negative"})
            assert len(scoreTemp1) > 0 and len(scoreTemp2) > 0, "No Pos / Neg scores found"
            scoreTemp3 = int(scoreTemp1[0].text)
            scoreTemp4 = int(scoreTemp2[0].text)
            with open(boostedFolder + "/" + "totals" + ".txt", "a") as g:
                g.write(nowTime + "," + item.permalink + "," + scoretotal + "," + str(scoreTemp3) + "," + str(scoreTemp4) + "\n")
                g.close()

        #todo find thread on the hot threads list

        time.sleep(2)


if __name__ == "__main__":

    nowTime = datetime.now().strftime("%H:%M:%S")
    currentFolder = incrementFolder(1)

    getfrontpage(1)
    controlGroup, boostedGroup = selectXthreadsNewest()
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

    import sendafakevote

    #Do fake votes here
    sessionList = []

    for user in sendafakevote.users:
        session = sendafakevote.loginFunction(user)
        sessionList.append(session)
    sendafakevote.numVotestoApply = 1
    sendafakevote.voteDirection = 1
    assert len(sessionList) >= sendafakevote.numVotestoApply, "Not enough users available to apply this number of votes1"
    assert len(sendafakevote.users) >= sendafakevote.numVotestoApply, "Not enough users available to apply this number of votes2"

    if len(sendafakevote.users) > sendafakevote.numVotestoApply:
        sendafakevote.users = sendafakevote.users[:sendafakevote.numVotestoApply]
        sessionList = sessionList[:sendafakevote.numVotestoApply]

    for item in boostedGroup:
        sendafakevote.urlToVote = item.permalink
        for user, session in zip(sendafakevote.users, sessionList):
            voteResponse = sendafakevote.applyVote(sendafakevote.urlToVote, session, sendafakevote.voteDirection, user)
            print("Got vote response: " + str(voteResponse))
            assert voteResponse == 200, 'Voting failed! Sound the alarm'
            time.sleep(2)

        print("Voting done!")
        print("Url Voted on: " + sendafakevote.urlToVote)
        print("Total users voted: " + str(sendafakevote.numVotestoApply))
        print("Vote direction: " + ("down" if sendafakevote.voteDirection == 0 else "up"))

    timesrun = 0
    for timesrun in range(0,24):
        time.sleep(300 - time.time() % 300)
        fiveMinScrape(currentFolder)
        print("Scraping again. 5 minute intervals. Current time is: " + nowTime)

    for timesrun in range(0,132):
        time.sleep(600 - time.time() % 600)
        fiveMinScrape(currentFolder)
        print("Scraping again. 10 minute intervals. Current time is: " + nowTime)

    print("All done scraping for 24 hours. Toodles")
    # < 288


