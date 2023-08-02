import csv
from Requirements import *
import os
import ast
import pandas as pd
# import AssistAPIInformationGetter

def delete_empty_rows(csv_file, output_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file, sep='\t')

    # Drop rows with all NaN (empty) values
    df.dropna(how='all', inplace=True)

    # Write the modified DataFrame back to a new CSV file
    df.to_csv(output_file, index=False, sep='\t')





UniNameShort = ["CSUF", "Sonoma","CPSLO", "Chico", "CSUSM", "SDSU", "SJSU", "CSULA", "CSUMB", "CSUN", "CSUB", "CSUSB", "CSUDH", "CSUEB", "CSUStan", "CSUS"
                , "SFSU", "Humboldt", "CSUFresno", "CSULB", "CSUCI", "CPP", "UCI", "UCB", "UCSD", "UCM", "UCSC", "UCSB", "UCD", "UCLA", "UCR"]
UnisQuarter = []
UnisSemester = []
CCsQuarter = []
CCsSemester = []
# CCsName = AssistAPIInformationGetter.getUniqueCCNamelst()


# deletes unnessary rows(does special things for different schools)
def FixCSV(uniName, CSVFileName):
    

    with open("csvs/UniSheets/" + uniName + "temp.csv", 'w') as fixedCSV:
        writer = csv.writer(fixedCSV, delimiter='\t')
        
        with open(CSVFileName + ".csv", 'r') as csvfile:
            
            reader = csv.reader(csvfile, delimiter='\t')
           
            prevCC = ''
            coursecnt = 0
            for row in reader:
                isrepeat = False
                for key in CCsdups.keys():
                    if row[0] == CCsdups[key]:
                        isrepeat = True
                        break
                if isrepeat:
                    continue
                # print(row)
                if row[0] == '':
                    continue
                if prevCC != row[0]:
                    # if row[0] == "Palomar College":
                    #     # print("resetting coursecnt")
                    coursecnt = 0
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
    delete_empty_rows("csvs/UniSheets/" + uniName + "temp.csv", "csvs/UniSheets/" + uniName + ".csv")
    os.remove("csvs/UniSheets/" + uniName + "temp.csv")    
def Fixall(UniList):
    for i in UniList:
        # print(i)
        FixCSV(i, "csvs/csvs/Assist PDF scraped agreements - " + i)
        
# [['CSE 12 - Basic Data Structures and Object-Oriented Design (4.00)', 'somthing']]
# Fixall(UniNameShort)
def getListfromString(str):
    
    return ast.literal_eval(str)


def getrelList(UniName):
    Reqs = []
    with open("csvs/ReqRelationships.csv", 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            # print(row[0])
            if row[0] == UniName:
                # print(row[1])
                # print(row[1])
                Reqs.append(getListfromString(row[1]))
    return Reqs
# print(getrelList("UCI"))
def getallRelatedCourses(reqlist):
    courses = []
    for i in reqlist:
        for j in i:
            for z in j:
                courses.append(z)
    return courses
# Fixes the format of the csv to capture full requirements
# relList format: [[cse 8A, CSE 8B], [CSE 11]]
def ConvertToGradReqs(CSVFileName, relList, UniName):
    # create a new CSV file for the final sheet
    AddedFromrelList = []
    artslist= []
    
    prevCC = ""
    with open("csvs/UniSheets/"+ UniName + "Gradreqs.csv", 'w') as csvfinal:
        writer = csv.writer(csvfinal, delimiter='\t')
        # open the scraped csv file
        with open(CSVFileName + ".csv", 'r') as csvr:
            reader = csv.reader(csvr, delimiter='\t')
            # iterate through the scraped csv file
            for row in reader:
                # if row[1] == "MATH 3B - Calculus with Applications, Second Course (4.00)":
                #     print("I see it")
                # print(row, UniName)
                isrepeat = False
                if row[0] != prevCC:
                    # print(AddedFromrelList)
                    for i in range(len(AddedFromrelList)):
                        writer.writerow([prevCC, AddedFromrelList[i], artslist[i]])
                    AddedFromrelList = []
                    artslist= []
                    
                # check if the req courses are in the rel list
                # rel list will be : [[['CSE 12 - Basic Data Structures and Object-Oriented Design (4.00)']], [['CSE 15L - Software Tools and Techniques Laboratory (2.00)']]]
                if row[1] == "MATH 3B - Calculus with Applications, Second Course (4.00)":
                    print("curr rel list: ", AddedFromrelList)
                for i in relList:
                    for j in i:
                        if row[1] in j:
                            
                            if row[1] not in getallRelatedCourses(AddedFromrelList):
                                if row[1] == "MATH 3B - Calculus with Applications, Second Course (4.00)":
                                    print("being added new")
                                AddedFromrelList.append(i)
    
                                artslist.append([getListfromString(row[2])])
                            else:
                                if row[1] == "MATH 3B - Calculus with Applications, Second Course (4.00)":
                                    print("being added to end of one")
                                artslist[len(artslist) - 1].append(getListfromString(row[2]))
                # if UniName == "CSUFresno" and "Evergreen" in row[0]:
                #     print(artslist)
                                
                prevCC = row[0]
            for i in range(len(AddedFromrelList)):
                writer.writerow([prevCC, AddedFromrelList[i], artslist[i]])
# ConvertToGradReqs("csvs/UniSheets/" + "CSUFresno", getrelList("CSUFresno"), "CSUFresno")
def ConvertAllUniToGradReqs(uniList):
    for uni in uniList:          
        ConvertToGradReqs("csvs/UniSheets/" + uni, getrelList(uni), uni)
# ConvertAllUniToGradReqs(UniNameShort)                               


