# from ProcessFile import *
from Requirements import *
import sys
#absolute path for the assist web scraping folder
sys.path.insert(1, 'C:/Users/a2576/Documents/GitHub/TransferPathways/AssistWebScraping')
import ProcessFile
from AssistAPIInformationGetter import *
from writeToCSV import *
import statistics
import pandas as pd
import numpy as np
import math
keyterms = ['']
renamedcolleges=['']
#A is known as B
#A
#B 
#A B
CCids = getCCIdList()
# print(CCids)
UCSDReq = {"cs": [["CSE 8A - Introduction to Programming and Computational Problem Solving I (4.00)", "CSE 8B - Introduction to Programming and Computational Problem Solving II (4.00)" ], 
                  ["CSE 11 - Introduction to Programming and Computational Problem Solving - Accelerated Pace(4.00)"], ["CSE 12 - Basic Data Structures and Object-Oriented Design (4.00) "], 
                  ["CSE 15L - SoftwareTools and Techniques Laboratory (2.00)"], ["CSE 20 - Discrete Mathematics (4.00) Same-As: MATH 15A"], ["CSE 21 - Mathematics for Algorithms and Systems (4.00)"],
                  ["CSE 30 - Computer Organization and Systems Programming (4.00)"]], 
            "math":[["MATH 18 - Linear Algebra (4.00)"], ["MATH 20A - Calculus for Scienceand Engineering (4.00)"], 
                  ["MATH 20B - Calculus for Scienceand Engineering (4.00)"], ["MATH 20C - Calculus and Analytic Geometry for Science and Engineering (4.00)"]]}

# list of the stats: goes [mean, median, max, min]
statsOverall = [0, 0, 0, 0]
statsCs = [0,0,0,0]
statsMath = [0,0,0,0]


df = pd.read_csv("./csvs/Assist_UCSD.csv", header=None)
row = df.shape[0]
print(row)
# print(df.iloc[-1,0])

dict = {}
totalnoncount = 0
totalrows = 0
firstone = 0
gap = 0
#count how many rows are needed for one cc
def gaprow(df, row):
    gap = 0
    firstccname = df.iloc[0,0]
    for i in range(row):
        ccname = df.iloc[i,0]
        if(ccname is np.nan or ccname == firstccname):
            gap = gap + 1
        else:
            break
    return gap
print("gap is " + str(gaprow(df, row)))
numcc = round(row/(gaprow(df,row)))
print("number of cc is " + str(((row+1)/(gaprow(df,row)))))
firstccname = df.iloc[0,0]
for i in range(row):
    ccname = df.iloc[i,0]
    if(ccname is np.nan or ccname == firstccname):
        gap = gap+1
    else:
        break
print(gap)

for i in range(row):
    ccname = df.iloc[i,0]
    if(ccname is np.nan):
        continue
    else:
        totalrows = totalrows + 1
        if(ccname not in list(dict.keys())):

            dict[ccname] = 0
            firstone = 1
        #makes sure it does not add twice
        if 'No Course Articulated' not in df.iloc[i,2] and firstone == 1:
            dict[ccname] = dict[ccname] + 1
            totalnoncount=totalnoncount+1
print (dict)
print()
print("number of non no articulated classes " + str(totalrows - totalnoncount))
cnt = dict.values()
print(len(dict.keys()))
# print(len(set(dict.keys())))
print(len(set(dict.keys())) == numcc and len(set(dict.keys())) == len(dict.keys()))
# # cnt = []
# # all the cc names in the csv file
# CCnames = df.iloc[:,0]
# CCnames = set(CCnames)
# CCnames.remove(np.nan)

# CCids = []
# for cc in CCnames:
#     print(cc)
#     CCids.append(getSchoolID(cc))

# print(CCnames)
# print(CCids)

# for i in range (len(CCnames)):
#     if( is Nan):
#         continue
#     else()
    
# print(CCnames)
# keys = []
# for cc in CCnames:
#     if cc in CCids:
#         keys.append(cc)
# for CC in CCids:
#     # retrieve the first column of the dataframe which is the cc name
#     if(CC == getSchoolID(df.iloc[:,0])):
#         print(1)


statsOverall[0] = statistics.mean(cnt)
statsOverall[1] = statistics.median(cnt)
statsOverall[2] = max(cnt)
statsOverall[3] = min(cnt)


#school, mean number of articulations, median number of articulations, max number of 
print("UCSD:  ")
print(statsOverall)