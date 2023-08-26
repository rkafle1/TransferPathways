import re
import csv
import CSVHandling
import numpy
import matplotlib.pyplot as plt
# list of phrases that show that a requirement is not articulated
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
# get the number of units from a course
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
# Generates a csv with all the CCs the uni has agreements with and writes to it the mappings of only the met grad reqs
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
                    courses = dictreqs[row[0]][len(dictreqs[row[0]]) - 1]
                   
                    if len(courses) == 0 or courses[1] > getUnits(option) or (courses[1] == getUnits(option) and courses[3] < (getUnits(option) - subtractfromoption)):
                            artUnitcnt = 0
                           
                            for metcourse in option:
                                if metcourse not in reldict.keys():
                                    continue
                                artUnitcnt += getUnits(bestOption(reldict[metcourse]))
                                    
                            dictreqs[row[0]][len(dictreqs[row[0]]) - 1] = [option, getUnits(option), artUnitcnt, getUnits(option) - subtractfromoption]

    return dictreqs

def AllListsofMetReqs(UniList):
    with open("csvs/Findings/MetReqs.csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for uni in UniList:   
            
            dictreqs = getMetReqs(uni)
            for key in dictreqs.keys():
                for req in dictreqs[key]:
                   
                    writer.writerow([uni, key, req])  

# Translates the requirements into grad reqs   
def TranslateReqsToGradReqs():
    wholetranslation = {}
    AllListsofMetReqs(CSVHandling.UniNameShort)
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
# translates the uni names                 
def TranslateUniNames(GradreqUniName):
    UniNamesinGradreqs = {'UC Berkeley BA':'UCB', 'UC Davis':'UCD', 'UC Irvine':'UCI', 'UC Los Angeles':'UCLA', 'UC Merced':'UCM', 'UC Riverside':'UCR', 'UC San Diego':'UCSD', 'UC Santa Cruz BS': 'UCSC', 'UC Santa Barbara':'UCSB', 'CSU Los Angeles':'CSULA', 'CSU Fullerton':'CSUF', 'CSU Channel Islands':'CSUCI', 'Chico State':'Chico', 'CSU Dominguez Hills':'CSUDH', 'CSU East Bay':'CSUEB', 'Fresno State':'CSUFresno', 'CP Humboldt':'Humboldt', 'CSU Long Beach':'CSULB', 'CSU Northridge': 'CSUN', 'CP Pomona':'CPP', 'Sacramento State':'CSUS', 'CSU San Bernardino':'CSUSB', 'San Diego State':'SDSU', 'San Francisco State':'SFSU', 'San Jose State':'SJSU', 'CSU San Marcos':'CSUSM', 'Stainislaus State':'CSUStan', 'Sonoma State':'Sonoma', 'CP San Luis Obispo':'CPSLO', 'CSU Bakersfield':'CSUB', 'CSU Monterey Bay':'CSUMB'}
    if GradreqUniName not in UniNamesinGradreqs.keys():
        return "not"
    return UniNamesinGradreqs[GradreqUniName]

# gets the best option's unit count
def getbestreqUnits(reqliststr):
    bestOptionsunits = 0
    reqlst = CSVHandling.getListfromString(reqliststr)
    for req in reqlst:
        bestOptionsunits +=  getUnits(bestOption(req))

# calculates the percentage of reqs of a certain type that met and generates a csv that contains the left over requirements of that type
# and the percentage of met reqs, and the number of leftover requirements and leftover courses
# loop through rows and if in met dict then don't add to the corrsponding list. for each uni cnt the number of requireements
# when you finish a uni add the rows for each CC and calculate the percentage: reqcnt - len(met reqs lst)/reqcnt
def LeftoverGradReqs(Reqtype):
    
    AssisttoGradTranslation = TranslateReqsToGradReqs()
    with open("./csvs/Findings/LeftoverGradReqs" + Reqtype + ".csv", 'w') as leftovercsv:
        writer = csv.writer(leftovercsv, delimiter='\t')
        writer.writerow(["University", "Community Collge", "Precentage of Units Articulated", "Unmet Requirements", "Met Units", "Total Units"])
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
                    if "Total units: 0" == row[1]:
                        continue
                    for CC in AssisttoGradTranslation[TranslateUniNames(row[0])].keys():
                        if TranslateUniNames(row[0]) in CSVHandling.semester:
                            
                            rows.append([TranslateUniNames(row[0]), CC, MetUnits[CC]/(TotalUnits[CC]),  UnmetCCReqs[CC], 1.5 * MetUnits[CC], 1.5 * TotalUnits[CC]])
                        else: 
                           
                            rows.append([TranslateUniNames(row[0]), CC, MetUnits[CC]/(TotalUnits[CC]), UnmetCCReqs[CC], MetUnits[CC], TotalUnits[CC]])
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
                        print(row[1])
                        TotalUnits[CC] += getUnits(bestOption(CSVHandling.getListfromString(row[1])))

                

               
                        
# def getbestvia2types(Reqtypes):
#     Reqtype1Percents = {}
#     Reqtype2Percents = {}
#     with open("./csvs/Findings/LeftoverGradReqs" + Reqtypes[0] + ".csv", 'w') as leftovercsv:
#         reader = csv.reader(leftovercsv, delimiter='\t')

# custom comparator where you compare the median percentage of met reqs
def agreementrankingcomparator(row):
    return float(row[2])

# Goes through the leftoverGradreqs csv and ranks the agreements on median percentage
def RankAgreementsperuni(reqtype):
    rankings = {}
    with open("./csvs/Findings/LeftoverGradReqs" + reqtype + ".csv") as leftovercsv:
        reader = csv.reader(leftovercsv, delimiter='\t')
        for row in reader:
            if len(row) == 0 or row[0] == "University":
                continue
            if row[0] not in rankings.keys():
                rankings[row[0]] = []
            rankings[row[0]].append(row)
    with open("./csvs/Findings/AgreementRankings" + reqtype +".csv", 'w') as rank:
        writer = csv.writer(rank, delimiter='\t')
        for uni in rankings.keys():
            sortedlst = sorted(rankings[uni], key=agreementrankingcomparator, reverse=True)
            writer.writerows(sortedlst)
# some more custom comparators
def agreementcomparator(row):
    return float(row[2])
def statcomparator(row):
    return float(row[1])
# this function calculates various aspects of the data and puts it into csv files
def rankAgreements(reqtype):
    rankings = []
    numberof1s = {}
    numberof0s = {}
    UnisStats = {}
    percentof1sCCs = {}
    CCStats = {}
    totalnumagg = 0
    with open("./csvs/Findings/AgreementRankings" + reqtype +".csv") as rank:
        reader = csv.reader(rank, delimiter='\t')
        for row in reader:

            if len(row) == 0: 
                continue
            totalnumagg += 1
            if row[0] not in numberof0s.keys():
                numberof0s[row[0]] = [0]
            if row[1] not in percentof1sCCs.keys():
                percentof1sCCs[row[1]] = [0, 0]
                CCStats[row[1]] = []
            if row[0] not in numberof1s.keys():
                numberof1s[row[0]] = [0, 0]
                UnisStats[row[0]] = []
            if float(row[2]) == 1:
                numberof1s[row[0]][0] += 1
                percentof1sCCs[row[1]][0] += 1
            percentof1sCCs[row[1]][1] += 1
            CCStats[row[1]].append(float(row[2]))
            UnisStats[row[0]].append(float(row[2]))
            numberof1s[row[0]][1] += 1
            rankings.append(row)
    # print(UnisStats.keys())
    rankings = sorted(rankings, key=agreementcomparator, reverse=True)  
    with open("./csvs/Findings/RankofallAgreements" + reqtype +".csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(rankings)
    with open("./csvs/Findings/Numberof1sUnis" + reqtype +".csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["University", "Percent of Agreements that are fully covered", "Number of fully covered agreements"])
        for uni in numberof1s.keys():
            writer.writerow([uni, numberof1s[uni][0]/numberof1s[uni][1], numberof1s[uni][0]])
    with open("./csvs/Findings/CoverageStatsUnis" + reqtype +".csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        rows = []
        writer.writerow(["University", "Median coverage", "Max coverage", "Min coverage", "Q1", "Q2", "IQR"])
        for uni in UnisStats.keys():
            
            rows.append([uni, numpy.median(UnisStats[uni]), max(UnisStats[uni]), min(UnisStats[uni]), numpy.percentile(UnisStats[uni], 25), numpy.percentile(UnisStats[uni], 75), numpy.percentile(UnisStats[uni], 75) - numpy.percentile(UnisStats[uni], 25)])
        sortedrow = sorted(rows, key=statcomparator, reverse=True)
        writer.writerows(sortedrow)
    with open("./csvs/Findings/CoverageStatsCCs" + reqtype +".csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        rows = []
        writer.writerow(["Community College", "Median coverage", "Max coverage", "Min coverage", "Q1", "Q2", "IQR"])
        for cc in CCStats.keys():
            rows.append([cc, numpy.median(CCStats[cc]), max(CCStats[cc]), min(CCStats[cc]), numpy.percentile(CCStats[cc], 25), numpy.percentile(CCStats[cc], 75), numpy.percentile(CCStats[cc], 75) - numpy.percentile(CCStats[cc], 25)])
        sortedrow = sorted(rows, key=statcomparator, reverse=True)
        writer.writerows(sortedrow)
    with open("./csvs/Findings/Numberof1sCCs" + reqtype +".csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["Community College", "Percent of Agreements that are fully covered", "Number of fully covered agreements"])
        for CC in percentof1sCCs.keys():
            writer.writerow([CC, percentof1sCCs[CC][0]/percentof1sCCs[CC][1], percentof1sCCs[CC][0]])
    totalidealagreements = 0
    print(numberof1s)
    for uni in numberof1s.keys():
        # print(numberof1s[uni][0])
        totalidealagreements += numberof1s[uni][0]

        
