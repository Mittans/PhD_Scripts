import os
from pathlib import Path
import csv
import operator
import datetime

class episodeClass:
    def __init__(self):
        self.episode = ''
        self.controlTime = []
        self.boostedTime = []
        self.times = []


episodeContainers = []

ndictControl = {}
ndictBoosted = {}

completedFolders = '/home/dotty/donFinished/'

subfolders = [ f.path for f in os.scandir(completedFolders) if f.is_dir() ]
finalTotalsFile = open(completedFolders + "FinalTotals.txt", "w")
finalTotalsFile.write("Time (mins), Cont Score Tot, Boost Score Tot, Cont Num Comms, Boost Num Comms, Boost Num Negs, Cont Num Negs\n")

for x in subfolders:
    episode = x.split("/")[-1:][0]
    episode1 = episodeClass()
    episode1.episode = episode
    paths = sorted(Path(x).iterdir(), key=os.path.getmtime)
    paths = list(filter(lambda y: Path(y).is_dir(), paths))
    for y in paths:
        totalsControlFile = open(str(y) + "/control/totals.txt", "r")
        totalsBoostedFile = open(str(y) + "/boosted/totals.txt", "r")
        csvtotalsControlFile = csv.reader(totalsControlFile)
        csvtotalsBoostedFile = csv.reader(totalsBoostedFile)
        #totalsControlFile.close()
        #totalsBoostedFile.close()
        for line in csvtotalsControlFile:
            if episode not in ndictControl.keys():
                ndictControl[episode] = (int(line[2]), int(line[3]), int(line[4]), int(line[5]))
            else:
                ndictControl[episode] = tuple(map(operator.add, ndictControl[episode], (int(line[2]), int(line[3]), int(line[4]), int(line[5]))))

        for line in csvtotalsBoostedFile:
            if episode not in ndictBoosted.keys():
                ndictBoosted[episode] = (int(line[2]), int(line[3]), int(line[4]), int("-99"))
            else:
                ndictBoosted[episode] = tuple(map(operator.add, ndictBoosted[episode], (int(line[2]), int(line[3]), int(line[4]), int("-99"))))

        episode1.controlTime.append(ndictControl[episode])
        episode1.boostedTime.append(ndictBoosted[episode])
        episode1.times.append(line[0])
        totalsControlFile.close()
        totalsBoostedFile.close()
        ndictControl = {}
        ndictBoosted = {}

    episodeContainers.append(episode1)



    #print(episode1)
timesrun = []
i = 0
for x in range(0,24):
    timesrun.append(str(i))
    i += 5
for y in range(0,132):
    timesrun.append(str(i))
    i += 10

for item in episodeContainers:
    csvstring = ""
    finalTotalsFile.write(item.episode + "\n")

    for item2, item3, time1 in zip(item.controlTime, item.boostedTime, timesrun):
        csvstring = time1 + ',' + str(item2[0]) + "," + str(item3[0])
        csvstring += ","
        csvstring += str(item2[3]) + "," + str(item3[3]) + ","
        csvstring += str(item2[2]) + "," + str(item3[2])
        csvstring += '\n'
        finalTotalsFile.write(csvstring)
finalTotalsFile.close()

print("hello")