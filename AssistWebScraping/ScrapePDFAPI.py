from ProcessFile import *
from writeToCSV import *
from Requirements import *

def dictFromAggreement(UniName, CCName):
    if "University of California, Irvine" in UniName:
        return CreateDictfromtxtIrvine(UniName, CCName, UCIReq)
    if "San Diego State University" in UniName:
        return DictFromTxtSDSU(UniName, CCName, SDSUReq)

    
def CSVForAllAggreements(UniName):
    CClst = getCCListWithAggreements(UniName)
    for cc in CClst:
        dict = dictFromAggreement(UniName, cc)
        generateCSVfromAgreement(dict, UniName, cc)

def MergeCSVs(UniName):
    CClst = getCCListWithAggreements(UniName)
    MergeUniversityCSVs(UniName, CClst)