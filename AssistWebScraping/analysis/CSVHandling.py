import csv


# deletes unnessary rows(does special things for different schools)
def FixCSV(uniName, CSVFileName):

    if uniName == 'UCI':
        return 0


# Fixes the format of the csv to capture full requirements
# relList format: [[cse 8A, CSE 8B], [CSE 11]]
def ConvertToGradReqs(CSVFileName, relList, UniName):
    # create a new CSV file for the final sheet
    AddedFromrelList = []
    with open(CSVFileName + "_Final.csv", 'w') as csvfinal:
        # open the scraped csv file
        with open(CSVFileName + ".csv", 'r') as csv:
            reader = csv.reader(csv)
            # iterate through the scraped csv file
            for row in reader:
                # check if the req courses are in the rel list
                for i in relList:
                    for j in i:
                        if row[1] in j:
                            
            # if so handle the relationship and write to new csv
            # else write that row to the new csv
            # add units in list form to 4th col.
    # Delete any blank rows
    # delete old csv file(scraped one)
