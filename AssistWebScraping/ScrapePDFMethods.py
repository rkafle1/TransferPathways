from ProcessFilefin import *
from writeToCSV import *
from Requirements import *

# calls the function to scrape the agreement and put it into a dictionary
# reqdict is the dictionary in Requirements for the university
def dictFromAggreement(UniName, CCName, reqdict):
    if "California State University, Long Beach" in UniName:
        return DictFromTxtCSULB(UniName, CCName, reqdict)
    else: 
        return DictFromTxtUnis(UniName, CCName, reqdict)

# creates a CSV with the agreement mappings for all agreements for UniName
# 1 csv per agreement   
def CSVForAllAggreements(UniName, reqdict):
    CClst = getCCListWithAggreements(UniName)
    for cc in CClst:
        try: 
            with open("agreements/report_" + str(getSchoolID(UniName)) +"_" + str(getSchoolID(cc))+"_CS.pdf") as f:
                dict = dictFromAggreement(UniName, cc, reqdict)
                print(dict, cc)
                generateCSVfromAgreement(dict, UniName, cc)

        except FileNotFoundError:
            continue
       
# merge all the agreement mappings into 1 csv
def MergeCSVs(UniName):
    CClst = getCCListWithAggreements(UniName)
    MergeUniversityCSVs(UniName, CClst)