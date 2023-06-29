import csv
from AssistAPIInformationGetter import *

def generateCSVfromAgreement(dict, UniversityName, CCName):
    fileName = "csvs/agreements/from" + CCName + "to" + UniversityName + ".csv"
    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        keys = dict.keys()
        for key in keys:
            row = [CCName, key, dict[key]]
            writer.writerow(row)
        
        # writer = csv.DictWriter(f, fieldnames=dict.keys())
        # writer.writeheader()
        # writer.writerow(dict)


def MergeUniversityCSVs(UniName, CCList):
    with open("csvs/" + UniName + ".csv", 'a') as f:
        writer = csv.writer(f)
        for cc in CCList:
            fileName = "csvs/agreements/from" + cc + "to" + UniName + ".csv"
            with open(fileName, 'r') as aggreement:
                reader = csv.reader(aggreement)
                for row in reader:
                    writer.writerow(row)
