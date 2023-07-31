from requirement import *
import csv
import CSVHandling
# generates list of the requirements met by an agreement for all CCs
def GetListofMetReqs(UniName):
    df = pd.read_csv("csvs/UniSheets/"+UniName+"Gradreqs.csv", header=None, sep='\t')
    row, column = df.shape
    # print(row, column)
    # print(df.iloc[0,1])
    # print(df.iloc[0,2])
    dictreqs = {}
   
    for i in range(row):
        ccName = df.iloc[i,0]
        courseName = df.iloc[i,1]
        logical_exp = convert_to_logical_expression(convert_to_numerical(ast.literal_eval(courseName)))
        # print(logical_exp)
        articulationName = df.iloc[i,2]
        booleanlists = []
        for item in (ast.literal_eval(articulationName)):
            exp = convert_to_logical_expression(convert_to_boolean(item))
            # print(eval(exp))
            booleanlists.append(eval(exp))
        finalans = substitute_with_bool(logical_exp, booleanlists)
        # print(eval(finalans))
        if "Choose" in courseName or "choose" in courseName:
            Req = CSVHandling.getListfromString(courseName)
            articulation = CSVHandling.getListfromString(articulationName)
            numofcourses = int(Req[0][0][len(Req[0][0]) - 1])
            articulatedcoursescnt = 0
            for art in articulation:
                if art[0][0] in nolist:
                    continue
                else:
                    articulatedcoursescnt += 1
            if ccName not in list(dictreqs.keys()):
                dictreqs[ccName]= []
            if articulatedcoursescnt >= numofcourses:
                dictreqs[ccName].append(courseName)
                continue

        if(ccName is np.nan):
            continue
        else:
            if(ccName not in list(dictreqs.keys())):
                dictreqs[ccName]= []
                if eval(finalans) == True:
                    dictreqs[ccName].append(courseName)
                    # print(ccName, "requirement met", " in line ", 2*i+1 )
                    
                firstone = True
            else:
                if eval(finalans) == True:
                    dictreqs[ccName].append(courseName)
                    # print(ccName, "requirement met", " in line ", 2*i-1 )
                
    return dictreqs      

# produces dicts of met requirements for all unis and puts it into a csv
def AllListsofMetReqs(UniList):
    with open("csvs/Findings/MetReqs.csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for uni in UniList: 
            print(uni)    
            dictreqs = GetListofMetReqs(uni)
            for key in dictreqs.keys():
                for req in dictreqs[key]:
                   
                    writer.writerow([uni, key, req])  

# print(GetListofMetReqs('UCI')) 
# AllListsofMetReqs(CSVHandling.UniNameShort)    

# Translates assit reqs to grad reqs and creates list of grad reqs met for each CC. Returns a dictionary: key = CCname value = list of grad reqs met
def TranslateReqsToGradReqs():
    # CSVHandling.delete_empty_rows("./csvs/ReqRelationships.csv", "./csvs/ReqRelationships.csv")
    CSVHandling.delete_empty_rows("./csvs/Findings/MetReqs.csv", "./csvs/Findings/MetReqs.csv")
    with open("./csvs/ReqRelationships.csv") as relcsv:
        with open("./csvs/Findings/MetReqs.csv") as metcsv:
            relreader = csv.reader(relcsv, delimiter='\t')
            metreader= csv.reader(metcsv, delimiter='\t')
            translation = {}
            WholeTranslation = {}
            prevCC = ""
            prevUni = ""
            MetReqsLst = []
            for row in metreader:
                if row[0] != prevUni:
                    WholeTranslation[row[0]] = {}
                if prevCC != row[1]:
                    WholeTranslation[row[0]][row[1]] = [row[2]]
                else:
                    WholeTranslation[row[0]][row[1]].append(row[2])
                prevCC = row[1]
                prevUni = row[0]
            for row in relreader:
                for CC in WholeTranslation[row[0]].keys():
                    reqlst = WholeTranslation[row[0]][CC]
                    for i in range(len(reqlst)):
                        
                        if reqlst[i] in row[1]:
                            reqlst[i] = row[2]
                    WholeTranslation[row[0]][CC] = reqlst
    return WholeTranslation 
# dict = TranslateReqsToGradReqs()
# print(dict["UCSD"]["Palomar College"])                    

dict = TranslateReqsToGradReqs()
print(dict["UCB"]["Evergreen Valley College"])                    
def TranslateUniNames(GradreqUniName):
    UniNamesinGradreqs = {'UC Berkeley BA':'UCB', 'UC Davis':'UCD', 'UC Irvine':'UCI', 'UC Los Angeles':'UCLA', 'UC Merced':'UCM', 'UC Riverside':'UCR', 'UC San Diego':'UCSD', 'UC Santa Cruz BS': 'UCSC', 'UC Santa Barbara':'UCSB', 'CSU Los Angeles':'CSULA', 'CSU Fullerton':'CSUF', 'CSU Channel Islands':'CSUCI', 'Chino State':'Chico', 'CSU Dominguez Hills':'CSUDH', 'CSU East Bay':'CSUEB', 'Fresno State':'CSUFresno', 'Cal Poly Humboldt':'Humboldt', 'CSU Long Beach':'CSULB', 'CSU Northridge': 'CSUN', 'Cal Poly Pomona':'CPP', 'Sacramento State':'CSUS', 'CSU San Bernardino':'CSUSB', 'San Diego State':'SDSU', 'San Francisco State':'SFSU', 'San Jose State':'SJSU', 'CSU San Marcos':'CSUSM', 'Stainislaus State':'CSUStan', 'Sonoma State':'Sonoma', 'Cal Poly San Luis Obispo':'CPSLO', 'CSU Bakersfield':'CSUB', 'CSU Monterey Bay':'CSUMB'}
    if GradreqUniName not in UniNamesinGradreqs.keys():
        return "not"
    return UniNamesinGradreqs[GradreqUniName]

# calculates the percentage of reqs of a certain type are met and generates a csv that contains the left over requirements of that type
# and the percentage of met reqs, and the number of leftover requirements and leftover courses

# loop through rows and if in met dict then don't add to the corrsponding list. for each uni cnt the number of requireements
# when you finish a uni add the rows for each CC and calculate the percentage: reqcnt - len(met reqs lst)/reqcnt
def LeftoverGradReqs(Reqtype):
    
    AssisttoGradTranslation = TranslateReqsToGradReqs()
    with open("./csvs/Findings/LeftoverGradReqs" + Reqtype + ".csv", 'w') as leftovercsv:
        writer = csv.writer(leftovercsv, delimiter='\t')
        # CSVHandling.delete_empty_rows("C:/Users/richa/OneDrive/Documents/GitHub/TransferPathwaysTool/graduationReqs/gradReqs" + Reqtype + ".csv", "C:/Users/richa/OneDrive/Documents/GitHub/TransferPathwaysTool/graduationReqs/gradReqs" + Reqtype + ".csv")
        with open("C:/Users/richa/OneDrive/Documents/GitHub/TransferPathwaysTool/graduationReqs/gradReqs" + Reqtype + ".csv") as gradreqcsv:
            reader = csv.reader(gradreqcsv)
            # rows has all the CCs info: percentage of met reqs and list of unmet reqs
            # format: rows = [[UniName, CC, pecentage, [unmetreqs]], ...]
            rows = []
            totalreqcnt = 0
            UnmetCCReqs = {}
            ismet = False
            for row in reader: 
                ismet = False
                if TranslateUniNames(row[0]) == "not":
                    continue
                if "Total courses" in row[1]:
                    if "UC Berkeley" in row[0]:
                        print(AssisttoGradTranslation[TranslateUniNames(row[0])].keys())
                    for CC in AssisttoGradTranslation[TranslateUniNames(row[0])].keys():
                        if "Contra Costa" in CC and "Berkeley" in row[0]:
                            print(UnmetCCReqs[CC])
                        rows.append([TranslateUniNames(row[0]), CC, (totalreqcnt - len(UnmetCCReqs[CC]))/totalreqcnt, UnmetCCReqs[CC]])
                        # if "UC Berkeley" in row[0]:
                            # print(len(UnmetCCReqs[CC]))
                            # print(UnmetCCReqs[CC])
                            # print(totalreqcnt)
                           
                    writer.writerows(rows)
                    rows = []
                    metCCReqs = {}
                    totalreqcnt = 0
                    continue
                # iterate through the CCs to see which CCs meet the row[1] req
                # print(row[0])
                for CC in AssisttoGradTranslation[TranslateUniNames(row[0])].keys():
                    if CC not in UnmetCCReqs.keys():
                        UnmetCCReqs[CC] = []
                    # Check if the req is met
                    for req in AssisttoGradTranslation[TranslateUniNames(row[0])][CC]:
                        if req in row[1] or row[1] in req:
                            # Courses = BreakintoCourses(req)
                            ismet = True
                            break 

                    if ismet == False and row[1] not in UnmetCCReqs[CC]:
                        UnmetCCReqs[CC].append(row[1])
                            
                totalreqcnt += 1
                prevUni = row[0]
        
                
            # for CC in AssisttoGradTranslation[TranslateUniNames(row[0])].keys():
            #     rows.append([prevUni, CC, (totalreqcnt - len(UnmetCCReqs[CC]))/totalreqcnt], UnmetCCReqs[CC])
            # writer.writerows(rows)
                            
                            
                # if ismetreq == False:

LeftoverGradReqs("LowerCS")     


                