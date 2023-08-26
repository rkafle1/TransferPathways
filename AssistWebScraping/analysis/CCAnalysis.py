import CSVHandling
import csv
import AssistAPIInformationGetter
import matplotlib.pyplot as plt

'''
This file deals with analysis of CCs specifically
'''
# counts the number of CCs a university has recent agreements with and provides a list
def GetCCswithRecentAgreement(UniName):
    with open("csvs/UniSheets/" + UniName + "Gradreqs.csv", 'r') as unicsv:
        reader = csv.reader(unicsv, delimiter='\t')
        prevCC = ""
        cnt = 0
        CCs = []
        for row in reader:
            if len(row) == 0:
                continue

            if row[0] != prevCC and ']' not in row[0] and row[0] not in CCs:
                if row[0] not in CSVHandling.CCsName:
                    continue
                cnt += 1
                CCs.append(row[0])
            prevCC = row[0]
    # CCs is the list of CCs it has a 2022-2023 agreement with
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
# Generates a bar graph displaying the cnts of agreements
def GenerateAgreementcntBarGraphUni():
    Unis = []
    Numofagreement = []
    NumofAgreementsUCs = {}
    NumofAgreementsCSUs = {}
    with open("csvs/Findings/RecentAgreementAnalysis.csv") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) == 0:
                continue
            if "UC" in row[0][0:2]:
                NumofAgreementsUCs[row[0]] = int(row[1])
            else:
                NumofAgreementsCSUs[row[0]] = int(row[1])
        
        for UC in NumofAgreementsUCs.keys():
            Unis.append(UC)
            Numofagreement.append(NumofAgreementsUCs[UC])
        for CSU in NumofAgreementsCSUs.keys():
            Unis.append(CSU)
            Numofagreement.append(NumofAgreementsCSUs[CSU])
        fullcnt = 0
        for i in Numofagreement:
            if i == 112:
                fullcnt += 1
        print(fullcnt, len(Numofagreement), fullcnt/len(Numofagreement))
        plt.bar(Unis, Numofagreement)
        plt.xlabel('University')
        plt.ylabel('Number of 2022-2023 Articulation Agreements')
        plt.title('Number of Recent Articulation Agreements Across Universities')
        plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
        plt.xticks(fontsize=5)
        plt.ylim(0, 112)
        
        plt.savefig('figures/RecentAgreementsUnisbar.png', dpi=700)