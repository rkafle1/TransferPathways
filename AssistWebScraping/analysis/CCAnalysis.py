import CSVHandling
import csv
import AssistAPIInformationGetter

# counts the number of CCs a university has recent agreements with and provides a list of those CCs
def GetCCswithRecentAgreement(UniName):
    
    with open("csvs/UniSheets/" + UniName + "Gradreqs.csv", 'r') as unicsv:
        reader = csv.reader(unicsv, delimiter='\t')
        prevCC = ""
        cnt = 0
        CCs = []
        for row in reader:
            if len(row) == 0:
                continue
            if "Madera" in row[0]:
                print(row[0])
            if row[0] != prevCC and ']' not in row[0] and row[0] not in CCs:
                cnt += 1
                CCs.append(row[0])
            prevCC = row[0]
        
    return [UniName, cnt, CCs]

# custom compartor for ranking Uni or CCs with most number of recent agreements
def compare(UniRow):
    return UniRow[1]

# calls getCCswithRecentAgreeent on all unis and puts it into a csv with the unis going from most CCs to least:
def GetAllUnisCCcnts(UniList):
    with open("csvs/Findings/RecentAgreementAnalysis.csv", 'w') as findingCSV:
        writer = csv.writer(findingCSV, delimiter='\t')
        Rows = []
        for i in UniList: 
            Rows.append(GetCCswithRecentAgreement(i))
        RowsSorted = sorted(Rows, key=compare, reverse=True)
        writer.writerows(RowsSorted)
# ranks the CCs on the number of universities they have recent agreements with
def RankCCsOnNumberofAgreements(CCList):
    cnts = [0 for _ in range(len(CCList))]
    Unis = [[] for _ in range(len(CCList))]
    rows = []
    CSVHandling.delete_empty_rows("csvs/Findings/RecentAgreementAnalysis.csv", "csvs/Findings/RecentAgreementAnalysis.csv")
    with open("csvs/Findings/RecentAgreementAnalysis.csv", 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                for i in range(len(CCList)):
                    if CCList[i] in CSVHandling.getListfromString(row[2]):
                        cnts[i] = cnts[i] + 1
                        Unis[i].append(row[0])
    for i in range(len(CCList)):
        rows.append([CCList[i], cnts[i], Unis[i]])
    sortedRows = sorted(rows, key=compare, reverse=True)
    with open("csvs/Findings/RecentAgreementAnalysisCCsRanking.csv", 'w') as CCcsv:
        writer = csv.writer(CCcsv, delimiter='\t')
        writer.writerows(sortedRows)

def GenerateAgreementcntBarGraphUni():
    Unis = []
    NumofAgreements = []
    with open("csvs/Findings/RecentAgreementAnalysis.csv") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) == 0:
                continue

GetAllUnisCCcnts(CSVHandling.UniNameShort)
RankCCsOnNumberofAgreements(AssistAPIInformationGetter.getCCNameList())


                
