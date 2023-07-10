from ProcessFile import *
from writeToCSV import *
from Requirements import *
from ProcessFileUCs import *

def dictFromAggreement(UniName, CCName):
    if "University of California, Irvine" in UniName:
        return DictFromTxtUCI(UniName, CCName, UCIReq)
    if "San Diego State University" in UniName:
        return DictFromTxtSDSU(UniName, CCName, SDSUReq)
    if "California State University, San Marcos" in UniName:
        return DictFromTxtCSUSM(UniName, CCName, CSUSMReq)
    if "California State University, Long Beach" in UniName:
        return DictFromTxtCSULB(UniName, CCName, CSULBReq)
    if "California State University, Bakersfield" == UniName:
        return DictFromTxtCSUB(UniName, CCName, CSUBReq)
    if "California State University, Channel Islands" in UniName:
        return DictFromTxtCSUCI(UniName, CCName, CSUCIReq)
    if "California State University, Fullerton" in UniName:
        return DictFromTxtCSUF(UniName, CCName, CSUFReq)
    if "California State University, Los Angeles" in UniName:
        return DictFromTxtCSULA(UniName, CCName, CSULAReq)
    if "California State University, San Bernardino" in UniName:
        return DictFromTxtCSUSB(UniName, CCName, CSUSBReq)
    if "California Polytechnic University, Pomona" in UniName:
        return DictFromTxtCPP(UniName, CCName, CPPReq)
    if "California State University, Dominguez Hills" in UniName:
        return DictFromTxtCSUDH(UniName, CCName, CSUDHReq)
    if "California State University, East Bay" in UniName:
        return DictFromTxtCSUEB(UniName, CCName, CSUEBReq)
    if "California State University, Fresno" in UniName:
        return DictFromTxtCSUFres(UniName, CCName, CSUFresnoReq)
    if "California Polytechnic University, Humboldt" in UniName:
        return DictFromTxtHumboldt(UniName, CCName, HumboldtReq)
    if "California Polytechnic University, San Luis Obispo" in UniName:
        return DictFromTxtCPSLO(UniName, CCName, CPSLOReq)
    if "California State University, Monterey Bay" in UniName:
        return DictFromTxtCSUMB(UniName, CCName, CSUMBReq)
    if "California State University, Northridge" in UniName:
        return DictFromTxtCSUN(UniName, CCName, CSUNReq)
    if "California State University, Sacramento" in UniName:
        return DictFromTxtCSUS(UniName, CCName, CSUSReq)
    if "California State University, Stanislaus" in UniName:
        return DictFromTxtCSUStan(UniName, CCName, CSUStanReq)
    if "San Francisco State University" in UniName:
        return DictFromTxtSFSU(UniName, CCName, SFSUReq)
    if "San Jose State University" in UniName:
        return DictFromTxtSJSU(UniName, CCName, SJSUReq)
    if "Sonoma State University" in UniName:
        return DictFromTxtSonoma(UniName, CCName, SonomaReq)
    if "California State University, Chico" in UniName:
        return DictFromTxtChico(UniName, CCName, ChicoReq)
    if "University of California, Davis" in UniName:
        return DictFromTxtUCD(UniName, CCName, UCDReq)
    if "University of California, Los Angeles" in UniName:
        return DictFromTxtUCLA(UniName, CCName, UCLAReq)
    if "University of California, Riverside" in UniName:
        return DictFromTxtUCR(UniName, CCName, UCRReq)
    if "University of California, San Diego" in UniName:
        return DictFromTxtUCSD(UniName, CCName, UCSDReq)
    if "University of California, Berkeley" in UniName:
        return DictFromTxtUCB(UniName, CCName, UCBReq)
    if "University of California, Santa Cruz" in UniName:
        return DictFromTxtUCSC(UniName, CCName, UCSCReq)
    if "University of California, Santa Barbara" in UniName:
        return DictFromTxtUCSB(UniName, CCName, UCSBReq)
    if "University of California, Merced" in UniName:
        return DictFromTxtUCM(UniName, CCName, UCMReq)

    
def CSVForAllAggreements(UniName):
    CClst = getCCListWithAggreements(UniName)
    
    for cc in CClst:
        try: 
            with open("agreements/report_" + str(getSchoolID(UniName)) +"_" + str(getSchoolID(cc))+"_CS.pdf") as f:
                dict = dictFromAggreement(UniName, cc)
                print(dict, cc)
                generateCSVfromAgreement(dict, UniName, cc)

        except FileNotFoundError:

            continue
       

def MergeCSVs(UniName):
    CClst = getCCListWithAggreements(UniName)

    MergeUniversityCSVs(UniName, CClst)