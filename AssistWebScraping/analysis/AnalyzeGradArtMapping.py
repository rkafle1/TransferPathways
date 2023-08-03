from requirement import *
import re
import csv
import CSVHandling

import matplotlib.pyplot as plt
nolist =    ['No Course Articulated', 
            'This course must be taken at the university after transfer',
            'Course(s) Denied', 
            'Not Articulated',
            'No Comparable Course',
            'No Articulation Established',
            'Articulates as Course-to-Course Only',
            'Articulates as a Series Only',
            'Articulation Pending Review',
            'No Current Articulation' 
        ]
# get Units from a course
def getUnits(Courselst):
    unitcnt = 0
    pattern = r"\(\w{1}\.\w{2}\)"
    for course in Courselst:
        all_units = re.findall(pattern, course)
        for unit in all_units:
            unitcnt += float(unit[1:len(unit) - 1])
    return unitcnt
# gets the mapping of course/1 req per arrow requirement and articulating course(s)
def getrel(Unireq, articulations, cc):
    reldict = {}
    Unireqlst = CSVHandling.getListfromString(Unireq)
    Artlst = CSVHandling.getListfromString(articulations)
    if "Citrus College" == cc:
        print(Unireqlst[0])
    reqcnt = 0
    for reqlst in Unireqlst:
        for req in reqlst:
            if reqcnt < len(Artlst):
                reldict[req] = Artlst[reqcnt]
                reqcnt += 1
            else: 
                return reldict
    return reldict
# gets the best articulation option for a certain req
def bestOption(artoptions):
    best = artoptions[0]
    for option in artoptions:
        if getUnits(best) > getUnits(option):
            best = option
 
    return best

# def getMetUnits(UniName):
#     Unitdict = {}
#     with open("csvs/UniSheets/"+UniName+"Gradreqs.csv") as f:
        
#         reader = csv.reader(f, delimiter='\t')
#         for row in reader:
#             if len(row) == 0:
#                 continue
#             NotArticulated = False
#             for noartphrase in requirement.nolist:
#                 if noartphrase in row[2]:
#                     NotArticulated = True
#                     break
            
#             if NotArticulated == False:
#                 reldict = getrel(row[1], row[2])
#                 reqlst = CSVHandling.getListfromString(row[1])
#                 if row[0] not in Unitdict.keys():
#                     Unitdict[row[0]] = []
#                 Unitdict[row[0]].append([])
#                 reqoptions = {}
#                 for option in reqlst:
#                     reqoptions[str(option)] = 0
#                     for req in option:
                        
#                         if req not in reldict.keys():
#                             print("i'm about to continue", req)
#                             continue
                        
#                         for noartphrase in requirement.nolist:
#                             if noartphrase in reldict[req]:
#                                 NotArticulated = True
#                                 break
#                         if NotArticulated == True:
#                             break
#                         else:
#                             reqoptions[str(option)] += getUnits(req)
#                 bestoption = 0
#                 for option in reqoptions.keys():
#                     if reqoptions[option] > bestoption:
#                         bestoption = reqoptions[option]
#                 Unitdict[row[0]][len(Unitdict[row[0]]) - 1] = [option, reqoptions[option]]




# generates list of the requirements met by an agreement for all CCs and the option it fullfills(CC courses and Uni courses)(adds up units if needed)
# generates list of the requirements met by an agreement for all CCs and the option it fullfills(CC courses and Uni courses)(adds up units if needed)
# dictreqs: key = CCName, val: [[req met by CC(specifically the courses/option that meets it), Uniunits to fullfill option, CC units to fullfill option,]]
def getMetReqs(UniName):
    dictreqs = {}
    CSVHandling.delete_empty_rows("csvs/UniSheets/"+UniName+"Gradreqs.csv", "csvs/UniSheets/"+UniName+"Gradreqs.csv")
    with open("csvs/UniSheets/"+UniName+"Gradreqs.csv") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            reldict = {}
            NotArticulated = False
            # for noartphrase in requirement.nolist:
            #     if noartphrase in row[2]:
            #         NotArticulated = True
            #         break
            if True:
                print(row)
                reldict = getrel(row[1], row[2], row[0])
                reqlst = CSVHandling.getListfromString(row[1])
                if row[0] not in dictreqs.keys():
                    dictreqs[row[0]] = []
                dictreqs[row[0]].append([])
                if "Choose" in reqlst[0][0] or "choose" in reqlst[0][0]:
                        # articulation
                        articulation = CSVHandling.getListfromString(row[2])
                        numofcourses = int(reqlst[0][0][len(reqlst[0][0]) - 1])
                        articulatedcoursescnt = 0
                        artunits = 0
                        for art in articulation:
                            if art[0][0] not in nolist:
                                artunits += getUnits(bestOption(art))
                                articulatedcoursescnt += 1
                            if articulatedcoursescnt == numofcourses:
                                break
                        if row[0] not in dictreqs.keys():
                            dictreqs[row[0]]= []
                        if articulatedcoursescnt > 0:
                            ChosenReqs = [] 
                            reqUnits = 0
                            for i in range(articulatedcoursescnt):
                                if len(ChosenReqs) < numofcourses:
                                    ChosenReqs.append(reqlst[i + 1])
                                    reqUnits += getUnits(reqlst[i + 1])
                            idealunits = 0
                            for i in range(numofcourses):
                                idealunits += getUnits(reqlst[i + 1])
                            dictreqs[row[0]].append([reqlst[1], idealunits, artunits, reqUnits])
                            continue

                for option in reqlst:
                    subtractfromoption = 0

                    for req in option:
                        if req not in reldict.keys():
                            continue
                        NotArticulated = False
                   
                            
            
                        if req not in reldict.keys():
                            continue
                        
                        for noartphrase in nolist:
                            if noartphrase in str(reldict[req]):
                                print(getUnits([req]))
                                subtractfromoption += getUnits([req])
                                
                            # if NotArticulated:
                            #     break

                    courses = dictreqs[row[0]][len(dictreqs[row[0]]) - 1]
                    
                    if len(courses) == 0 or courses[1] > getUnits(option) or (courses[1] == getUnits(option) and courses[3] < (getUnits(option) - subtractfromoption)):
                            artUnitcnt = 0
                           
                            for metcourse in option:
                                if metcourse not in reldict.keys():
                                    continue
                                artUnitcnt += getUnits(bestOption(reldict[metcourse]))
                                    
                            dictreqs[row[0]][len(dictreqs[row[0]]) - 1] = [option, getUnits(option), artUnitcnt, getUnits(option) - subtractfromoption]

    return dictreqs
# getMetReqs("UCM")
# def GetListofMetReqs(UniName):
#     df = pd.read_csv("csvs/UniSheets/"+UniName+"Gradreqs.csv", header=None, sep='\t')
#     row, column = df.shape
#     # print(row, column)
#     # print(df.iloc[0,1])
#     # print(df.iloc[0,2])
#     dictreqs = {}
   
#     for i in range(row):
#         ccName = df.iloc[i,0]
#         courseName = df.iloc[i,1]
#         logical_exp = convert_to_logical_expression(convert_to_numerical(ast.literal_eval(courseName)))
#         # print(logical_exp)
#         articulationName = df.iloc[i,2]
#         booleanlists = []
#         for item in (ast.literal_eval(articulationName)):
#             exp = convert_to_logical_expression(convert_to_boolean(item))
#             # print(eval(exp))
#             booleanlists.append(eval(exp))
#         finalans = substitute_with_bool(logical_exp, booleanlists)
#         # print(eval(finalans))
#         if "Choose" in courseName or "choose" in courseName:
#             Req = CSVHandling.getListfromString(courseName)
#             articulation = CSVHandling.getListfromString(articulationName)
#             numofcourses = int(Req[0][0][len(Req[0][0]) - 1])
#             articulatedcoursescnt = 0
#             for art in articulation:
#                 if art[0][0] in nolist:
#                     continue
#                 else:
#                     articulatedcoursescnt += 1
#             if ccName not in list(dictreqs.keys()):
#                 dictreqs[ccName]= []
#             if articulatedcoursescnt >= numofcourses:
#                 dictreqs[ccName].append(courseName)
#                 continue

#         if(ccName is np.nan):
#             continue
#         else:
#             if(ccName not in list(dictreqs.keys())):
#                 dictreqs[ccName]= []
#                 if eval(finalans) == True:
#                     dictreqs[ccName].append(courseName)
#                     # print(ccName, "requirement met", " in line ", 2*i+1 )
                    
#                 firstone = True
#             else:
#                 if eval(finalans) == True:
#                     dictreqs[ccName].append(courseName)
#                     # print(ccName, "requirement met", " in line ", 2*i-1 )
                
#     return dictreqs      

# produces dicts of met requirements for all unis and puts it into a csv
def AllListsofMetReqs(UniList):
    with open("csvs/Findings/MetReqs.csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for uni in UniList:   
            
            dictreqs = getMetReqs(uni)
            for key in dictreqs.keys():
                for req in dictreqs[key]:
                   
                    writer.writerow([uni, key, req])  

# print(GetListofMetReqs('UCI')) 
# AllListsofMetReqs(CSVHandling.UniNameShort)    
def TranslateReqsToGradReqs():
    wholetranslation = {}
    with open("./csvs/ReqRelationships.csv") as relcsv:
        translationdict = {}
        relreader = csv.reader(relcsv, delimiter='\t')
        for row in relreader:
            if row[0] not in translationdict.keys():
                translationdict[row[0]] = {}
            translationdict[row[0]][row[1]] = row[2]
   
    with open("./csvs/Findings/MetReqs.csv") as metcsv:
        metreader = csv.reader(metcsv, delimiter='\t')
        for row in metreader:
            if len(row) == 0:
                continue
            if row[0] not in wholetranslation.keys():
                wholetranslation[row[0]] = {row[1]:[]}
            elif row[1] not in wholetranslation[row[0]].keys():
                wholetranslation[row[0]][row[1]] = []
            reqlst = CSVHandling.getListfromString(row[2])
            if len(reqlst) == 0:
                continue
            if 0 == reqlst[3]:
                continue

            for reqstr in reqlst[0]:
                
                for key in translationdict[row[0]].keys():
                    # if row[0] == "UCSD" and row[1] == "Palomar College":
                    #     print(reqstr, key)
                    if reqstr in key:
                        translatereqname = key
            wholetranslation[row[0]][row[1]].append([translationdict[row[0]][translatereqname], float(reqlst[1]), float(reqlst[2]), float(reqlst[3])])
  
    
    return wholetranslation
TranslateReqsToGradReqs()
# Translates assit reqs to grad reqs and creates list of grad reqs met for each CC. Returns a dictionary: key = CCname value = list of grad reqs met
# def TranslateReqsToGradReqs():
#     # CSVHandling.delete_empty_rows("./csvs/ReqRelationships.csv", "./csvs/ReqRelationships.csv")
#     CSVHandling.delete_empty_rows("./csvs/Findings/MetReqs.csv", "./csvs/Findings/MetReqs.csv")
#     with open("./csvs/ReqRelationships.csv") as relcsv:
#         with open("./csvs/Findings/MetReqs.csv") as metcsv:
#             relreader = csv.reader(relcsv, delimiter='\t')
#             metreader= csv.reader(metcsv, delimiter='\t')
#             translation = {}
#             WholeTranslation = {}
#             prevCC = ""
#             prevUni = ""
#             MetReqsLst = []
#             for row in metreader:
#                 if row[0] != prevUni:
#                     WholeTranslation[row[0]] = {}
#                 if prevCC != row[1]:
#                     WholeTranslation[row[0]][row[1]] = [CSVHandling.getListfromString(row[2])]
#                 else:
#                     WholeTranslation[row[0]][row[1]].append(CSVHandling.getListfromString(row[2]))
#                 prevCC = row[1]
#                 prevUni = row[0]
            
#             print(WholeTranslation["UCSD"]["Palomar College"])
#             for row in relreader:
#                 for CC in WholeTranslation[row[0]].keys():
#                     reqlst = WholeTranslation[row[0]][CC]
#                     for i in range(len(reqlst)):
#                         if len(reqlst[i]) == 0:
#                             continue
#                         for req in reqlst[i][0]:
#                             if req in row[1] and row[2]:
#                                 reqlst[i] = [row[2], reqlst[i][1], reqlst[i][2]]
#                     WholeTranslation[row[0]][CC] = reqlst
#             print(WholeTranslation["UCSD"]["Palomar College"])
#     return WholeTranslation 
# dict = TranslateReqsToGradReqs()
# print(dict["UCSD"]["Palomar College"])                    

# dict = TranslateReqsToGradReqs()
# print(dict["UCSD"]["Evergreen Valley College"])                    
def TranslateUniNames(GradreqUniName):
    UniNamesinGradreqs = {'UC Berkeley BA':'UCB', 'UC Davis':'UCD', 'UC Irvine':'UCI', 'UC Los Angeles':'UCLA', 'UC Merced':'UCM', 'UC Riverside':'UCR', 'UC San Diego':'UCSD', 'UC Santa Cruz BS': 'UCSC', 'UC Santa Barbara':'UCSB', 'CSU Los Angeles':'CSULA', 'CSU Fullerton':'CSUF', 'CSU Channel Islands':'CSUCI', 'Chino State':'Chico', 'CSU Dominguez Hills':'CSUDH', 'CSU East Bay':'CSUEB', 'Fresno State':'CSUFresno', 'Cal Poly Humboldt':'Humboldt', 'CSU Long Beach':'CSULB', 'CSU Northridge': 'CSUN', 'Cal Poly Pomona':'CPP', 'Sacramento State':'CSUS', 'CSU San Bernardino':'CSUSB', 'San Diego State':'SDSU', 'San Francisco State':'SFSU', 'San Jose State':'SJSU', 'CSU San Marcos':'CSUSM', 'Stainislaus State':'CSUStan', 'Sonoma State':'Sonoma', 'Cal Poly San Luis Obispo':'CPSLO', 'CSU Bakersfield':'CSUB', 'CSU Monterey Bay':'CSUMB'}
    if GradreqUniName not in UniNamesinGradreqs.keys():
        return "not"
    return UniNamesinGradreqs[GradreqUniName]


def getbestreqUnits(reqliststr):
    bestOptionsunits = 0
    reqlst = CSVHandling.getListfromString(reqliststr)
    for req in reqlst:
        bestOptionsunits +=  getUnits(bestOption(req))
# calculates the percentage of reqs of a certain type are met and generates a csv that contains the left over requirements of that type
# and the percentage of met reqs, and the number of leftover requirements and leftover courses

# loop through rows and if in met dict then don't add to the corrsponding list. for each uni cnt the number of requireements
# when you finish a uni add the rows for each CC and calculate the percentage: reqcnt - len(met reqs lst)/reqcnt
def LeftoverGradReqs(Reqtype):
    
    AssisttoGradTranslation = TranslateReqsToGradReqs()
    with open("./csvs/Findings/LeftoverGradReqs" + Reqtype + ".csv", 'w') as leftovercsv:
        writer = csv.writer(leftovercsv, delimiter='\t')
        writer.writerow(["University", "Community Collge", "Precentage of Units Articulated", "Unmet Requirements", "Met Units", "Unmet Units"])
        # CSVHandling.delete_empty_rows("C:/Users/richa/OneDrive/Documents/GitHub/TransferPathwaysTool/graduationReqs/gradReqs" + Reqtype + ".csv", "C:/Users/richa/OneDrive/Documents/GitHub/TransferPathwaysTool/graduationReqs/gradReqs" + Reqtype + ".csv")
        with open("C:/Users/richa/OneDrive/Documents/GitHub/TransferPathwaysTool/graduationReqs/CSVs/gradReqs" + Reqtype + ".csv") as gradreqcsv:
            reader = csv.reader(gradreqcsv)
            # rows has all the CCs info: percentage of met reqs and list of unmet reqs
            # format: rows = [[UniName, CC, pecentage, [unmetreqs]], ...]
            rows = []
           
            MetUnits = {}
            UnmetCCReqs = {}
            TotalUnits = {}
            ismet = False
            for row in reader: 
                ismet = False
                # move onto the next row if it is an empty row or it is ex: eecs row, somthing articulations don't check
                if len(row) == 0 or TranslateUniNames(row[0]) == "not":
                    continue
                # gather and write out the rows for the university. Indicates that the reqs for a uni are done
                if "Total units" in row[1]:
                   
                    for CC in AssisttoGradTranslation[TranslateUniNames(row[0])].keys():
                        # print(row[0], CC, MetUnits[CC], Unmetunits)
                        # print(row[0], CC, MetUnits[CC], UnmetUnits[CC], UnmetCCReqs[CC])
                        if TranslateUniNames(row[0]) in CSVHandling.semester:
                            rows.append([TranslateUniNames(row[0]), CC, MetUnits[CC]/(TotalUnits[CC]),  UnmetCCReqs[CC], 1.5 * MetUnits[CC], 1.5 * TotalUnits[CC]])
                        else: 
                            rows.append([TranslateUniNames(row[0]), CC, MetUnits[CC]/(TotalUnits[CC]), UnmetCCReqs[CC], MetUnits[CC], TotalUnits[CC]])
                        # if "UC Berkeley" in row[0]:
                            # print(len(UnmetCCReqs[CC]))
                            # print(UnmetCCReqs[CC])
                            # print(totalreqcnt)
                           
                    writer.writerows(rows)
                    rows = []
                    UnmetCCReqs = {}
                    TotalUnits = {}
                    MetUnits = {}
                    continue
                # iterate through the CCs to see which CCs meet the row[1] req
                # print(row[0])
                for CC in AssisttoGradTranslation[TranslateUniNames(row[0])].keys():
                    ismet = False
                    if CC not in UnmetCCReqs.keys():
                        UnmetCCReqs[CC] = []
                        MetUnits[CC] = 0
                        TotalUnits[CC] = 0

                    # Check if the req is met
                    
                    for Metreq in AssisttoGradTranslation[TranslateUniNames(row[0])][CC]:
                        
                        if len(Metreq) == 0:
                            continue
                        if Metreq[0] in row[1]:
                            MetUnits[CC] += Metreq[3]
                            TotalUnits[CC] += Metreq[1]
                            if Metreq[3] < Metreq[1]:
                                UnmetCCReqs[CC].append(row[1])
                            ismet = True
                            break
                    if ismet == False:
                        UnmetCCReqs[CC].append(row[1])
                        TotalUnits[CC] += getUnits(bestOption(CSVHandling.getListfromString(row[1])))

                
                
                        # for req in CSVHandling.getListfromString(Metreq[0]):
                            
                        # #     for reqstr in req[0]:
                        # #         if reqstr in row[1]:
                        #             # print(req, row[1])
                        #             # Courses = BreakintoCourses(req)
                        #     if str(req) in row[1]:
                        #             print(row[1], req)
                        #             ismet = True
                        #             MetUnits[CC] += 1
    
               
                        
def getbestvia2types(Reqtypes):
    Reqtype1Percents = {}
    Reqtype2Percents = {}
    with open("./csvs/Findings/LeftoverGradReqs" + Reqtypes[0] + ".csv", 'w') as leftovercsv:
        reader = csv.reader(leftovercsv, delimiter='\t')

def GenerateScatterCOMB(Reqtypes):
    percentsreqtype2 = []
    percentsreqtype1 = []
    with open("./csvs/Findings/LeftoverGradReqs" + Reqtypes[0] + ".csv", 'w') as leftovercsv:
        reader = csv.reader(leftovercsv, delimiter='\t')
        for row in reader:
            percentsreqtype1.append(row[2] * 100)
    with open("./csvs/Findings/LeftoverGradReqs" + Reqtypes[1] + ".csv", 'w') as leftovercsv:
        reader = csv.reader(leftovercsv, delimiter='\t')
        for row in reader:
            percentsreqtype2.append(row[2] * 100)
    plt.scatter(percentsreqtype1, percentsreqtype2) 
    plt.xlabel(Reqtypes[0])
    plt.ylabel(Reqtypes[1])
    plt.title('Percentage of Graduation Requirement Units Covered by Agreements')   

   


                