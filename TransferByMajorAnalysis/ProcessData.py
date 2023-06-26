import pandas as pd
import numpy as np
# CCList is a list of each of the CC csv file names and CSVFile is the file you want to put the CS info in
def CreateCSV(CCList, CSVFile):
    with open(CSVFile, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for CC in CCList:
            with open(CC, 'r') as f:
                reader = csv.reader(f, delimiter='\t')
                for row in reader:
                    # if line_count = 0
                    if "Computer" in row[4] and "Science" in row[4]:
                        writethisrow = [CC.replace(".csv", ""), row[0]]
                        for i in range(5, len(row)):
                            if row[i] == '':
                                writethisrow.append(0)
                            else:
                                writethisrow.append(row[i])
                        writer.writerow(writethisrow)
                        break
CCList = ["CSVs/AllanHancock.csv", "CSVs/AmericanRiver.csv"]

# CreateCSV(CCList, "CSVs/CCDataProcessed.csv")

with open("CSVs/AllanHancock.tsv", 'r', errors='replace') as input_csv:
    reader = csv.reader(input_csv, delimiter='\t')

    for row in reader:
        
                

