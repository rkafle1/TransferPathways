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
import re
import sys

# Returns the minimum number courses that could be taken
def count_courses(line):
    OR = "],"
    AND = "',"

    l = line.split(OR)
    min_course_count = sys.maxsize

    for c in l:
        # find the index of each indication of an "AND'd" course. + 1 to include the course before the first comma
        num_of_ands = len([i.start() for i in re.finditer(AND, c)]) + 1
        if num_of_ands < min_course_count:
            min_course_count = num_of_ands

    if min_course_count == sys.maxsize:
        min_course_count = 0

    return min_course_count

def write_csv(csv_path, name, matches):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        if '.csv' not in name[-4:]:
            name += '.csv'
        
        with open(name, 'w') as new_file:
            csv_writer = csv.writer(new_file)
            course_count = 0

            # NOTE: This will skip first row
            first_row = next(csv_reader, None)

            # Check first row for keywords
            if any([x in first_row[1] for x in matches]):
                csv_writer.writerow(first_row)
                course_count += count_courses(first_row[1])
            
            # Get name of the school in the first row
            # NOTE: Assumes the first row has a school name
            prev_school = first_row[0]

            # Repeat above steps for the remaining rows
            for line in csv_reader:
                # Evaluates the second colomn with line[1]
                if any([x in line[1] for x in matches]):
                    # If a school has been fully evaluated, write total course count
                    if prev_school != line[0] and course_count > 0:
                        l = [prev_school, "Total courses: " + str(course_count)]
                        csv_writer.writerow(l)
                        course_count = 0
                    csv_writer.writerow(line)
                    course_count += count_courses(line[1])

                    prev_school = line[0]
            
            # get last schools course count
            l = [prev_school, "Total courses: " + str(course_count)]
            csv_writer.writerow(l)

if __name__ == '__main__':
    path      = input('Enter CSV file path: ')
    cs_name   = input('Enter desired name for CS CSV file: ')
    math_name = input('Enter desired name for math CSV file: ')
    sci_name  = input('Enter desired name for science CSV file: ')

    # Added space at the end of each abbreviation to ensure it checks only for the course numbers
    cs_matches   = ['CS ', 'CSE ', 'ECS ', 'EEC ', 'I&C ', 'IN4MATX ', 'COM SCI ', 'CMPSC ', 'CPSC ', 'COMP ', 'CSCI ', 'CSCI/MATH ', 'CSC ', 'CPE ', 'CECS ', 'CMPS ', 'CST ', 'ENGR ', 'ECE ']
    math_matches = ['Math ', 'MATH ', 'MAT ', 'PSTAT ', 'STATS ', 'STAT ', 'STA ', 'Discrete']
    sci_matches  = ['Physics ', 'PHYSICS ', 'PHYS ', 'PHY ', 'BIO ', 'BIOL ', 'CHEM ', 'CHE ', 'Chem ']

    write_csv(path, cs_name, cs_matches)
    write_csv(path, math_name, math_matches)
    write_csv(path, sci_name, sci_matches)
