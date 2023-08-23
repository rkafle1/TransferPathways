import csv
import re
import sys
import matplotlib.pyplot as plt
import numpy as np

# Returns the minimum number courses that could be taken
def count_courses(line):
    OR = "],"
    AND = "',"

    course_list = line.split(OR)
    min_course_count = sys.maxsize

    for course in course_list:
        # find the index of each indication of an "AND'd" course. + 1 to include the course before the first comma
        num_of_ands = len([i.start() for i in re.finditer(AND, course)]) + 1
        if num_of_ands < min_course_count:
            min_course_count = num_of_ands

    if min_course_count == sys.maxsize:
        return 0

    return min_course_count

def get_course_count(csv_path, exclude, count_dict):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        count = 0

        # NOTE: This will skip first row
        first_row = next(csv_reader, None)

        # Check first row for keywords
        if all(s not in first_row[1] for s in exclude):
            count += count_courses(first_row[1])
            
        # Get name of the school in the first row
        # NOTE: Assumes the first row has a school name
        prev_school = first_row[0]

        # Repeat above steps for the remaining rows
        for line in csv_reader:
            if (not line):
                continue
            # Evaluates the second colomn with line[1]
            # If a school has been fully evaluated, write total unit count
            if prev_school != line[0]:
                count_dict[prev_school] = count
                count = 0
            
            if all(s not in line[1] for s in exclude):
                count += count_courses(line[1])
            
            prev_school = line[0]
        
        # get last schools unit count
        count_dict[prev_school] = count

def count_units(line):
    units = "\d+\.\d+" # units will be floating point numbers

    # A -- is an indicator to just read the floating point at the end of the line
    if '--' in line:
        return float( re.findall(units, line)[0] )
    
    course_list = line.split("],")
    min_units_count = sys.maxsize

    for course in course_list:
        count = 0.0
        units_list = re.findall(units, course)

        for u in units_list:
            count += float(u)

        if count < min_units_count:
            min_units_count = count

    if min_units_count == sys.maxsize:
        return 0.0

    return min_units_count


def write_all(csv_path, name, count_dict):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        if '.csv' not in name[-4:]:
            name += '.csv'
        
        with open(name, 'w') as new_file:

            csv_writer = csv.writer(new_file)
            unit_count = 0

            # NOTE: This will skip first row
            first_row = next(csv_reader, None)
            csv_writer.writerow(first_row)
            unit_count += count_units(first_row[1])
            
            # Get name of the school in the first row
            # NOTE: Assumes the first row has a school name
            prev_school = first_row[0]

            # Repeat above steps for the remaining rows
            for line in csv_reader:
                # Evaluates the second colomn with line[1]
                if prev_school != line[0]:
                    csv_writer.writerow( [prev_school, "Total units: " + str(unit_count)] )
                    count_dict[prev_school] = unit_count
                    unit_count = 0

                csv_writer.writerow(line)
                unit_count += count_units(line[1])
                prev_school = line[0]
            
            # get last schools unit count
            csv_writer.writerow( [prev_school, "Total units: " + str(unit_count)] )
            count_dict[prev_school] = unit_count


def get_type_unit_count(csv_path, matches, exclude, count_dict):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        unit_count = 0

        # NOTE: This will skip first row
        first_row = next(csv_reader, None)

        # Check first row for keywords
        if any([x in first_row[1] for x in matches]):
            if all(s not in first_row[1] for s in exclude):
                unit_count += count_units(first_row[1])
            
        # Get name of the school in the first row
        # NOTE: Assumes the first row has a school name
        prev_school = first_row[0]

        # Repeat above steps for the remaining rows
        for line in csv_reader:
            # Evaluates the second colomn with line[1]
            
            # If a school has been fully evaluated, write total unit count
            if prev_school != line[0]:
                count_dict[prev_school] = unit_count
                unit_count = 0

            if any([x in line[1] for x in matches]):
                if all(s not in line[1] for s in exclude):
                    unit_count += count_units(line[1])

            prev_school = line[0]
        
        # get last schools unit count
        count_dict[prev_school] = unit_count


def write_type_unit_count(csv_path, name, matches, exclude, count_dict):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        if '.csv' not in name[-4:]:
            name += '.csv'
        
        with open(name, 'w') as new_file:

            csv_writer = csv.writer(new_file)
            unit_count = 0

            # NOTE: This will skip first row
            first_row = next(csv_reader, None)

            # Check first row for keywords
            if any([x in first_row[1] for x in matches]):
                if all(s not in first_row[1] for s in exclude):
                    csv_writer.writerow(first_row)
                    unit_count += count_units(first_row[1])
            
            # Get name of the school in the first row
            # NOTE: Assumes the first row has a school name
            prev_school = first_row[0]

            # Repeat above steps for the remaining rows
            for line in csv_reader:
                # Evaluates the second colomn with line[1]
                
                # If a school has been fully evaluated, write total unit count
                if prev_school != line[0]:
                    csv_writer.writerow( [prev_school, "Total units: " + str(unit_count)] )
                    count_dict[prev_school] = unit_count
                    unit_count = 0

                if any([x in line[1] for x in matches]):
                    if all(s not in line[1] for s in exclude):
                        csv_writer.writerow(line)
                        unit_count += count_units(line[1])

                prev_school = line[0]

            # get last schools unit count
            csv_writer.writerow( [prev_school, "Total units: " + str(unit_count)] )
            count_dict[prev_school] = unit_count


if __name__ == '__main__':

    # The course numbers of CS, math, and science courses from all UCs and CSUs.
    # Added space at the end of each abbreviation to ensure it checks only for the course numbers
    cs_matches   = ['CS ', 'CSE ', 'ECS ', 'EEC ', 'I&C ', 'IN4MATX ', 'COM SCI ', 'CMPSC ', 'CPSC ', 'COMP ', 'CSCI', 'CSCI/EECE ', 'CINS ', 'CSC ', 'CPE ', 'CECS ', 'CMPS ', 'CST ', 'ENG ', 'ENGR ', 'ECE ', 'EE ', 'Discrete ', 'Mathematical Structures I']
    math_matches = ['Math ', 'MATH ', 'MAT ', 'PSTAT ', 'STATS ', 'STAT ', 'STA ', 'E E ']
    sci_matches  = ['Physics ', 'physics', 'PHYSICS ', 'PHYS ', 'PHY ', 'BIO ', 'BIOL ', 'CHEM ', 'CHE ', 'Chem ', 'ELECTIVE SCIENCE:']
