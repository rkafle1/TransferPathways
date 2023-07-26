'''
Takes a CSV file of courses and puts CS, math, and science courses in their own CSV files.

Example input:

Enter CSV file path: gradReqsLOWER.csv
Enter desired name for CS CSV file: gradReqsLowerCS
Enter desired name for math CSV file: gradReqsLowerMATH
Enter desired name for science CSV file: gradReqsLowerSCI

This will put 3 new files in your current directory:
gradReqsLowerCS.csv, gradReqsLowerMATH.csv, and gradReqsLowerSCI.csv
'''

import csv

def write_csv(csv_path, name, matches):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        if '.csv' not in name[-4:]:
            name += '.csv'
        
        with open(name, 'w') as new_file:
            csv_writer = csv.writer(new_file)

            for line in csv_reader:
                # Evaluates the second colomn with line[1]
                if any([x in line[1] for x in matches]):
                    csv_writer.writerow(line)

if __name__ == '__main__':
    path      = input('Enter CSV file path: ')
    cs_name   = input('Enter desired name for CS CSV file: ')
    math_name = input('Enter desired name for math CSV file: ')
    sci_name  = input('Enter desired name for science CSV file: ')

    # Added space at the end of each abbreviation so that it checks for the course number
    cs_matches   = ['CS ', 'CSE ', 'ECS ', 'EEC ', 'I&C ', 'IN4MATX ', 'COM SCI ', 'CMPSC ', 'CPSC ', 'COMP ', 'CSCI ', 'CSCI/MATH ', 'CSC ', 'CPE ', 'CECS ', 'CMPS ', 'CST ', 'ENGR ', 'ECE ']
    math_matches = ['Math ', 'MATH ', 'MAT ', 'PSTAT ', 'STATS ', 'STAT ', 'STA ', 'Discrete']
    sci_matches  = ['Physics ', 'PHYSICS ', 'PHYS ', 'PHY ', 'BIO ', 'BIOL ', 'CHEM ', 'CHE ', 'Chem ']

    write_csv(path, cs_name, cs_matches)
    write_csv(path, math_name, math_matches)
    write_csv(path, sci_name, sci_matches)
