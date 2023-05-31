# from ProcessFile import *

import ProcessFile
from AssistAPIInformationGetter import *
from writeToCSV import *
import statistics

CCids = getCCIdList()
IrvineReq = {"cs": [["I&C SCI 31 - Introduction to Programming (4.00)", "I&C SCI 32 - Programming with Software Libraries (4.00)", "I&C SCI 33 - Intermediate Programming (4.00)"]],
             "math":[["MATH 2A - Single-Variable Calculus (4.00)"], ["MATH 2B - Single-Variable Calculus (4.00)"]], "1 additional": True}

# list of the stats: goes [mean, median, max, min]
statsOverall = [0, 0, 0, 0]
statsCs = [0,0,0,0]
statsMath = [0,0,0,0]

cnt = []
for CC in CCids:
    articulations = ProcessFile.CreateDictfromtxtUCI('agreements/report_120_' + str(CC) + '_CS.pdf', IrvineReq)
    # generateCSVfromAgreement(articulations, "csvs/agreements/report_120_" + str(CC) + "_CS.csv")
    keys = articulations.keys()
    cnt.append(0)
    for i in keys:
        reqarticulations = articulations[i]
        for j in reqarticulations:
            cnt[len(cnt) - 1] += len(j)

statsOverall[0] = statistics.mean(cnt)
statsOverall[1] = statistics.median(cnt)
statsOverall[2] = max(cnt)
statsOverall[3] = min(cnt)

print(statsOverall)