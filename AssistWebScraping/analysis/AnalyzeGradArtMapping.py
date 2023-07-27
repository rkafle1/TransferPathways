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
AllListsofMetReqs(CSVHandling.UniNameShort)    

# Translates assit reqs to grad reqs and creates list of grad reqs met for each CC
# def TranslateReqsToGradReqs(UniName):
#     with open 
