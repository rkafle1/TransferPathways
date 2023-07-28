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


# calculates the percentage of reqs of a certain type are met and generates a csv that contains the left over requirements of that type
# and the percentage of met reqs, and the number of leftover requirements and leftover courses
def LeftoverGradReqs(Reqtype):
    with open("./csvs/Findings/LeftoverGradReqs.csv", 'w') as leftovercsv:
        writer = csv.writer(leftovercsv, delimiter='\t')
        with open("graduationReqs/gradReqs" + Reqtype + ".csv") as gradreqcsv:
            reader = csv.reader(gradreqcsv)
            for row in reader:
                