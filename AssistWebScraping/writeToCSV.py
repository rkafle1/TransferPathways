import csv


def generateCSVfromAgreement(dict, fileName):
    with open(fileName, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=dict.keys())
        writer.writeheader()
        writer.writerow(dict)
