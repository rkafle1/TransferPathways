import csv
from Requirements import *
import os
import ast
import pandas as pd

'''
This file has various functions that are needed to analyze the assist scraped csvs that have been validated
'''

# various lists and dictionaries of information
# CCsdups shows the known as CCs
CCsdups = {"Compton College": "Compton Community College", "Santa Ana College": "Rancho Santiago College", "Reedley College":"Kings River College",
           "Berkeley City College":"Vista Community College"}
UniNameShort = ["CSUF", "Sonoma","CPSLO", "Chico", "CSUSM", "SDSU", "SJSU", "CSULA", "CSUMB", "CSUN", "CSUB", "CSUSB", "CSUDH", "CSUEB", "CSUStan", "CSUS"
                , "SFSU", "Humboldt", "CSUFresno", "CSULB", "CSUCI", "CPP", "UCI", "UCB", "UCSD", "UCM", "UCSC", "UCSB", "UCD", "UCLA", "UCR"]
# list of universities on the quarter and semester system
quarter = ["CPSLO", "UCI", "UCSD", "UCSC", "UCSB", "UCD", "UCLA", "UCR"]
semester = ["UCB", "UCM", "CSUF", "Sonoma", "Chico", "CSUSM", "SDSU", "SJSU", "CSULA", "CSUMB", "CSUN", "CSUB", "CSUSB", "CSUDH", "CSUEB", "CSUStan", "CSUS"
                , "SFSU", "Humboldt", "CSUFresno", "CSULB", "CSUCI", "CPP"] 
# if in semester multiply units by 1.5
# List of unique CCs
CCsName = ['Evergreen Valley College', 'Los Angeles City College', 'College of Marin', 'College of San Mateo', 'College of the Sequoias', 'Butte College',
            'Cerro Coso Community College', 'Columbia College', 'Merritt College', 'Cuesta College', 'Merced College', 'Las Positas College',
            'Victor Valley College', 'Barstow Community College', 'Los Angeles Trade Technical College', 'American River College', 'Contra Costa College',
            'College of the Desert', 'Los Angeles Harbor College', 'Mission College', 'City College of San Francisco', 'Fresno City College', 'Shasta College',
            'Lake Tahoe Community College', 'Cabrillo College', 'Glendale Community College', 'Los Angeles Valley College', 'San Diego Miramar College',
            'Los Angeles Mission College', 'Ohlone College', 'Pasadena City College', 'Foothill College', 'Modesto Junior College', 'Mt. San Jacinto College',
            'San Diego City College', 'Golden West College', 'Palomar College', 'Santa Rosa Junior College', 'Los Medanos College', 'Mount San Antonio College',
            'Palo Verde College', 'Rio Hondo College', 'Saddleback College', 'Santiago Canyon College', 'West Hills College Coalinga', 'Canada College',
            'Chaffey College', 'Crafton Hills College', 'Cypress College', 'Gavilan College', 'Napa Valley College', 'Orange Coast College', 'Laney College',
            'Riverside City College', 'West Valley College', 'Lassen Community College', 'College of the Redwoods', 'Bakersfield College',
            'Los Angeles Pierce College', 'Oxnard College', 'Yuba College', 'West Los Angeles College', 'Santa Barbara City College',
            'Sierra College', 'Solano Community College', 'Ventura College', 'Chabot College', 'Citrus College', 'Cuyamaca College', 'Mendocino College',
            'San Diego Mesa College', 'College of the Siskiyous', 'El Camino College', 'Cerritos College', 'Coastline Community College', 'Grossmont College',
            'Imperial Valley College', 'MiraCosta College', 'San Joaquin Delta College', 'Allan Hancock College', 'College of Alameda', 'Copper Mountain College',
            'De Anza College', 'Diablo Valley College', 'East Los Angeles College', 'Taft College', 'Antelope Valley College', 'Feather River College', 'Hartnell College',
            'Irvine Valley College', 'Porterville College', 'Sacramento City College', 'Skyline College', 'Los Angeles Southwest College', 'San Bernardino Valley College',
            'Monterey Peninsula College', 'Fullerton College', 'Long Beach City College', 'San Jose City College', 'Santa Monica College', 'Southwestern College', 'Moorpark College',
            'College of the Canyons', 'Cosumnes River College', 'Folsom Lake College', 'West Hills College Lemoore', 'Woodland Community College', 'Norco College', 'Moreno Valley College',
            'Clovis Community College', 'Compton College', 'Madera Community College', 'Santa Ana College', 'Reedley College', 'Berkeley City College']
# print(len(CCsName))
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
    os.remove("csvs/UniSheets/" + uniName + "temp.csv")    

# Fixes all universities
def Fixall(UniList):
    for i in UniList:
        # print(i)
        FixCSV(i, "csvs/csvs/Assist PDF scraped agreements - " + i)
        
# CSVs have lists which are stored as strings so this takes in that string and returns the list
def getListfromString(str):
    return ast.literal_eval(str)

# Gets a list of the requirements on assist that are also grad reqs
def getrelList(UniName):
    Reqs = []
    with open("csvs/ReqRelationships.csv", 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if row[0] == UniName:
                Reqs.append(getListfromString(row[1]))
    return Reqs
# Gets a list of courses contained in these requirments
# 1 req can be multiple courses
def getallRelatedCourses(reqlist):
    courses = []
    for i in reqlist:
        for j in i:
            for z in j:
                courses.append(z)
    return courses
# Writes to csvs/UniSheets/"+ UniName + "Gradreqs.csv" the requirements, as they appear on 
# the graduation reqs and adds the articulating CC courses
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
                prevCC = row[0]
            for i in range(len(AddedFromrelList)):
                writer.writerow([prevCC, AddedFromrelList[i], artslist[i]])
# Generates grad req mapping csvs for all universities
def ConvertAllUniToGradReqs(uniList):
    for uni in uniList:          
        ConvertToGradReqs("csvs/UniSheets/" + uni, getrelList(uni), uni)                              


