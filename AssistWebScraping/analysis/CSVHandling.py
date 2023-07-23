import csv
from Requirements import *

# deletes unnessary rows(does special things for different schools)
def FixCSV(uniName, CSVFileName):
    with open(CSVFileName + "fixed.csv", 'w') as fixedCSV:
        writer = csv.writer(fixedCSV)
        
        with open(CSVFileName + ".csv", 'r') as csv:
            reader = csv.reader(csv)
            prevCC = ''
            coursecnt = 0
            for row in reader:
                if row[0] == '':
                    continue
                if prevCC != row[0]:
                    coursecnt = 0
                if uniName == 'UCI' and row[1] == "One additional approved transferable course for the major (an":
                    continue
                if uniName == 'CPP':
                    # Choose2 = ['CS 2250 - Introduction to Web Science and Technology (3.00)', 'CS 2410 - Fundamentals of Data Science (3.00)', 'CS 2450 - User Interface Design and Programming (3.00)', 'CS 2520 - Python for Programmers (3.00)', 'CS 2560 - C++ Programming (3.00)']
                    for i in CPPReq["MAJOR REQUIRED ELECTIVES"]:
                        for j in range(len(i)):
                            
                            if i[j] in row[1] and coursecnt < 2:
                                if j == 4:
                                    writer.writerow(row)
                    continue


# Fixes the format of the csv to capture full requirements
# relList format: [[cse 8A, CSE 8B], [CSE 11]]
def ConvertToGradReqs(CSVFileName, relList, UniName):
    # create a new CSV file for the final sheet
    AddedFromrelList = []
    with open(CSVFileName + "_Final.csv", 'w') as csvfinal:
        # open the scraped csv file
        with open(CSVFileName + ".csv", 'r') as csv:
            reader = csv.reader(csv)
            # iterate through the scraped csv file
            for row in reader:
                # check if the req courses are in the rel list
                for i in relList:
                    for j in i:
                        if row[1] in j:
                            
            # if so handle the relationship and write to new csv
            # else write that row to the new csv
            # add units in list form to 4th col.
    # Delete any blank rows
    # delete old csv file(scraped one)
