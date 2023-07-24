import csv
from Requirements import *
import os
UniNameShort = ["CSUF", "Sonoma","CPSLO", "Chico", "CSUSM", "SDSU", "SJSU", "CSULA", "CSUMB", "CSUN", "CSUB", "CSUSB", "CSUDH", "CSUEB", "CSUStan", "CSUS"
                , "SFSU", "Humboldt", "CSUFresno", "CSULB", "CSUCI", "CPP", "UCI", "UCB", "UCSD", "UCM", "UCSC", "UCSB", "UCD", "UCLA", "UCR"]


# deletes unnessary rows(does special things for different schools)
def FixCSV(uniName, CSVFileName):
    with open("csvs/UniSheets/" + uniName + ".csv", 'w') as fixedCSV:
        writer = csv.writer(fixedCSV)

        with open(CSVFileName + ".csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            prevCC = ''
            coursecnt = 0
            for row in reader:
                if row[0] == '':
                    continue
                if prevCC != row[0]:
                    if row[0] == "Palomar College":
                        print("resetting coursecnt")
                    coursecnt = 0
                if row[0] == "Palomar College":
                    print(coursecnt)
                if uniName == 'UCI' and row[1] == "One additional approved transferable course for the major (an":
                    continue
                if uniName == 'CPP':
                    written = False
                    # Choose2 = ['CS 2250 - Introduction to Web Science and Technology (3.00)', 'CS 2410 - Fundamentals of Data Science (3.00)', 'CS 2450 - User Interface Design and Programming (3.00)', 'CS 2520 - Python for Programmers (3.00)', 'CS 2560 - C++ Programming (3.00)']
                    for i in CPPReq["MAJOR REQUIRED ELECTIVES"]:
                        for j in range(len(i)):
                            
                            if i[j] in row[1]:
                                if coursecnt < 2:
                                    if "[['Not Articulated']]" not in row[2] and "[['No Course Articulated']]" not in row[2]:
                                        writer.writerow(row)
                                        coursecnt += 1
                                    else:  
                                        if 'CS 2560 - C++ Programming (3.00)' in i[j]:
                                            writer.writerow(row)
                                            coursecnt += 1
                                        if 'CS 2520 - Python for Programmers (3.00)' in i[j] and coursecnt == 0:
                                            writer.writerow(row)
                                            coursecnt += 1
                                written = True
                    if written == False:
                        writer.writerow(row)
                    prevCC = row[0]
                    continue
                if uniName == "CSUDH":
                    
                    choose1 = ["CSC 251 - C Language Programming and UNIX (3.00)", "CSC 255 - Dynamic Web Programming (3.00)"]
                    if row[1] in choose1:
                        if coursecnt < 1:
                            if "[['No Course Articulated']]" not in row[2]:
                                writer.writerow(row)
                                coursecnt += 1
                            elif row[1] == choose1[1]:
                                writer.writerow(row)
                                coursecnt += 1
                    else:
                        writer.writerow(row)
                    prevCC = row[0]
                    continue
                if uniName == "CSUB":
                    written = False
                    for i in CSUBReq["Select 1 Course(s) from the following"]:
                        for j in range(len(i)):
                            if i[j] in row[1]:
                                if coursecnt < 1:
                                    if "[['Not Articulated']]" not in row[2] and "[['No Course Articulated']]" not in row[2]:
                                        writer.writerow(row)
                                        coursecnt += 1
                                    else:  
                                        if 'SCI 1409 - Introduction to Scientific Thinking (3.00)' in i[j]:
                                            writer.writerow(row)
                                            coursecnt += 1
                                written = True
                    if written == False:
                        writer.writerow(row)
                    prevCC = row[0]
                    continue
                writer.writerow(row)
                prevCC = row[0]
        
def Fixall(UniList):
    for i in UniList:
        FixCSV(i, "csvs/csvs/Assist PDF scraped agreements - " + i)
# [['CSE 12 - Basic Data Structures and Object-Oriented Design (4.00)', 'somthing']]
Fixall(UniNameShort)
def getListfromString(str):
 
    if '[' == str[0] or '"' == str[0]:
        lst = getListfromString(str[1:len(str) - 1])
    else:
        lst = []
        elementstart = -1
        for i in range(len(str)):
            if str[i] == "'" and elementstart == -1:
                elementstart = i

            elif str[i] == "'":
                lst.append(str[elementstart+1:i])
                elementstart
    


# def getrelList(UniName):
#     Reqs = []
#     with open("csvs/ReqRelationships.csv", 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             if row[0] == UniName:
                
# Fixes the format of the csv to capture full requirements
# relList format: [[cse 8A, CSE 8B], [CSE 11]]
# def ConvertToGradReqs(CSVFileName, relList, UniName):
#     # create a new CSV file for the final sheet
#     AddedFromrelList = []
#     with open(CSVFileName + "_Final.csv", 'w') as csvfinal:
#         # open the scraped csv file
#         with open(CSVFileName + ".csv", 'r') as csv:
#             reader = csv.reader(csv)
#             # iterate through the scraped csv file
#             for row in reader:
#                 # check if the req courses are in the rel list
#                 for i in relList:
#                     for j in i:
#                         if row[1] in j:

            # if so handle the relationship and write to new csv
            # else write that row to the new csv
            # add units in list form to 4th col.
    # Delete any blank rows
    # delete old csv file(scraped one)
