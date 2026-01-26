from os.path import isfile
import requests
import pickle
from datetime import datetime
from bs4 import BeautifulSoup as BSHTML
import time
import argparse



urlToVote = 'https://thedonald.win/p/3LK/'
numVotestoApply = 10





myUserAgent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
donVotingPage = 'https://thedonald.win/vote'

listofUsers = []

proxyUrl = dict(http='<redacted>',
                https='<redacted>')

loginUrl = 'https://thedonald.win/login'


voteDirection = 1


# direction 1 = upvote
# direction 0 = downvote
# _csrf:aa08feb7-f786-438e-ba6d-864e4e11c055

class voteUsers:
    def __init__(self, username='testusername', password='testpassword', proxyObj=None):
        if proxyObj is None:
            proxyObj = dict(http='testhttp', https='testhttps')
        self.username = username
        self.password = password
        self.proxyObj = proxyObj
        self.sessionFile = self.setdefaultSessionFile()

    def setdefaultSessionFile(self):
        return self.username + '.txt'

    def getdefaultSessionFile(self):
        return self.sessionFile


'''
Other proxies:
98.143.158.50
173.44.37.106
96.44.144.122
96.44.189.114
68.71.244.6
73.254.222.146

'''


users = []

users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))
users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))
users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))
users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))
users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))
users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))
users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))
users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))
users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))
users.append(voteUsers('<redacted>', '<redacted>',
                       dict(http='<redacted>',
                            https='<redacted>')))

def loginFunction(user: voteUsers) -> requests.session:
    foundStoredSession = False
    if isfile(user.sessionFile):
        print("Logging in")
        with open(user.sessionFile, "rb") as f:
            session = pickle.load(f)
        foundStoredSession = True
        print("Found log in for: " + user.username + " checking cookie expiry")
        for cookie in session.cookies:
            if cookie.expires == None: continue
            print(datetime.fromtimestamp(cookie.expires))
            thisNow = datetime.now().timestamp()
            if (cookie.expires + 86400) < int(datetime.now().timestamp()):
                print("Cookies expires soon, need to log in again")
                foundStoredSession = False
    if not foundStoredSession:
        session = requests.session()
        r = session.post(loginUrl,
                         data={'referrer': 'https://thedonald.win/', 'name': user.username, 'password': user.password,
                               'remember-me': 'true'}, proxies=user.proxyObj, headers=myUserAgent)
        foundStoredSession = False
        with open(user.sessionFile, "wb") as f:
            pickle.dump(session, f)
            f.close()
        assert r.status_code == 200, 'Login failed! Sound the alarm'
        print("New login for user " + user.username + " created and dumped to: " + user.sessionFile)
        time.sleep(3)
    return session


def applyVote(url, session, direction, user: voteUsers):
    votedirection = 1
    if direction == 'down' or direction == 0 or direction == 'downvote': votedirection = 0
    voteResponse = BSHTML(session.get(url, proxies=user.proxyObj, headers=myUserAgent).text, 'html.parser')
    csrf_token = voteResponse.find('input', attrs={'name': '_csrf'})['value']
    threadId = voteResponse.find('div', attrs={'data-type': 'post', 'class': 'post'})['data-id']
    votePostResponse = session.post(donVotingPage, data={'id': threadId, 'type': 'true', 'direction': str(direction),
                                                         '_csrf': csrf_token}, proxies=user.proxyObj,
                                    headers=myUserAgent)
    return votePostResponse.status_code


def testdaProxy():
    session = requests.get('http://www.bing.com', proxies=proxyUrl, headers=myUserAgent)
    return session


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Add specified number of votes to selected thread')
    parser.add_argument('--votes', type=int, default=10,
                        help='Number of votes to apply (max 10): integer')

    parser.add_argument('--url', type=str, required=True,
                        help='Url to apply the votes to')
    parser.add_argument('--direction', type=str, default='up', help='Direction to apply the votes (up / down)')
    args = parser.parse_args()
    print("Url given: " + args.url)
    print("Num votes to apply: " + str(args.votes))
    urlToVote = args.url
    numVotestoApply = args.votes

    sessionList = []
    numUsers = len(users)

    for user in users:
        session = loginFunction(user)
        sessionList.append(session)

    assert len(sessionList) >= numVotestoApply, "Not enough users available to apply this number of votes"
    assert len(users) >= numVotestoApply, "Not enough users available to apply this number of votes"

    if len(users) > numVotestoApply:
        users = users[:numVotestoApply]
        sessionList = sessionList[:numVotestoApply]

    for user, session in zip(users, sessionList):
        voteResponse = applyVote(urlToVote, session, voteDirection, user)
        print("Got vote response: " + str(voteResponse))
        assert voteResponse == 200, 'Voting failed! Sound the alarm'
        time.sleep(5)

    print("All done!")
    print("Url Voted on: " + urlToVote)
    print("Total users voted: " + str(numVotestoApply))
    print("Vote direction: " + ("down" if voteDirection == 0 else "up"))
