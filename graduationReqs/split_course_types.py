'''
Takes a CSV file of courses and puts CS, math, and science courses in their own CSV files.

Example input:

Enter CSV file path: CSVs/gradReqsLOWER.csv
Enter desired path/name for CS CSV file: CSVs/gradReqsLowerCS
Enter desired path/name for math CSV file: CSVs/gradReqsLowerMATH
Enter desired path/name for science CSV file: CSVs/gradReqsLowerSCI

This will put 3 new files in the folder "CSVs" in your current directory:
gradReqsLowerCS.csv, gradReqsLowerMATH.csv, and gradReqsLowerSCI.csv
'''

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


def count_units(line):
    units = "\d+\.\d+" # units will be floating point numbers

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

    # Added space at the end of each abbreviation to ensure it checks only for the course numbers
    cs_matches   = ['CS ', 'CSE ', 'ECS ', 'EEC ', 'I&C ', 'IN4MATX ', 'COM SCI ', 'CMPSC ', 'CPSC ', 'COMP ', 'CSCI', 'CSCI/EECE ', 'CINS ', 'CSC ', 'CPE ', 'CECS ', 'CMPS ', 'CST ', 'ENG ', 'ENGR ', 'ECE ', 'Discrete ']
    math_matches = ['Math ', 'MATH ', 'MAT ', 'PSTAT ', 'STATS ', 'STAT ', 'STA ', 'E E ']
    sci_matches  = ['Physics ', 'physics', 'PHYSICS ', 'PHYS ', 'PHY ', 'BIO ', 'BIOL ', 'CHEM ', 'CHE ', 'Chem ', 'ELECTIVE SCIENCE:']

    # Stacked graph (sort by value): math, science, lower cs, upper elective, upper required
    # Required vs Optional(Elective)

    lower_cs_count = {}
    lower_math_count = {}
    lower_sci_count = {}
    lower_other_count = {}
    get_type_unit_count('CSVs/gradReqsLOWER.csv', cs_matches  , sci_matches + ['Linear Algebra', 'Statistics'], lower_cs_count)
    get_type_unit_count('CSVs/gradReqsLOWER.csv', math_matches, sci_matches + ['Discrete'], lower_math_count)
    get_type_unit_count('CSVs/gradReqsLOWER.csv', sci_matches , [], lower_sci_count)
    get_type_unit_count('CSVs/gradReqsLOWER.csv', ['PHIL ', 'ENGL '], cs_matches + math_matches + sci_matches, lower_other_count)

    upper_cs_count = {}
    cs_elective_count = {}
    upper_math_count = {}
    upper_sci_count = {}
    upper_other_count = {}
    get_type_unit_count('CSVs/gradReqsUPPER.csv', cs_matches  , ['ELECTIVE:', 'Statistics', 'Probability'], upper_cs_count)
    get_type_unit_count('CSVs/gradReqsUPPER.csv', ['ELECTIVE: '], [], cs_elective_count)
    get_type_unit_count('CSVs/gradReqsUPPER.csv', math_matches, ['Discrete'], upper_math_count)
    get_type_unit_count('CSVs/gradReqsUPPER.csv', sci_matches , [], upper_sci_count)
    get_type_unit_count('CSVs/gradReqsUPPER.csv', ['PHIL ', 'ENGL ', 'ES/WGQS '], cs_matches + math_matches + sci_matches, upper_other_count)

    for school in lower_cs_count:
        if "UC" in school or "San Luis Obispo" in school:
            if "Berkeley" not in school and "Merced" not in school:
                lower_cs_count[school] /= 1.5
                lower_math_count[school] /= 1.5
                lower_sci_count[school] /= 1.5
                lower_other_count[school] /= 1.5
                upper_cs_count[school] /= 1.5
                cs_elective_count[school] /= 1.5
                upper_math_count[school] /= 1.5
                upper_sci_count[school] /= 1.5
                upper_other_count[school] /= 1.5

    lower_cs = list(lower_cs_count.values())
    upper_cs = list(upper_cs_count.values())
    elective_cs = list(cs_elective_count.values())

    lower_other = list(lower_other_count.values())
    upper_other = list(upper_other_count.values())
    other = list(np.add(lower_other, upper_other))

    lower_math = list(lower_math_count.values())
    upper_math = list(upper_math_count.values())
    math = list(np.add(lower_math, upper_math))

    lower_sci = list(lower_sci_count.values())
    upper_sci = list(upper_sci_count.values())
    science = list(np.add(lower_sci, upper_sci))

    labels = list(lower_cs_count.keys())

    plt.subplot().set_title('Unit Count of Major Required Courses')
    plt.bar(labels, lower_cs, label="Lower Division CS")
    plt.bar(labels, upper_cs, bottom=lower_cs, label="Required Upper Division CS")

    bot = list(np.add(lower_cs, upper_cs))
    plt.bar(labels, elective_cs, bottom=bot, label="Elective Upper Division CS")

    bot = list(np.add(bot, elective_cs))
    plt.bar(labels, math, bottom=bot, label="Math")

    bot = list(np.add(bot, math))
    plt.bar(labels, science, bottom=bot, label="Science")

    bot = list(np.add(bot, science))
    plt.bar(labels, other, bottom=bot, label="Other")

    plt.xticks(rotation='vertical')

    plt.legend()
    plt.show()

    '''
    lower_count = {}
    upper_count = {}

    write_all('CSVs/gradReqsLOWER.csv', 'CSVs/gradReqsLOWERCount.csv', lower_count)
    write_all('CSVs/gradReqsUPPER.csv', 'CSVs/gradReqsUPPERCount.csv', upper_count)

    lower_cs_count = {}
    lower_math_count = {}
    lower_sci_count = {}
    lower_other_count = {}
    write_type_unit_count('CSVs/gradReqsLOWER.csv', 'CSVs/gradReqsLowerCS'  , cs_matches  , sci_matches + ['Linear Algebra', 'Statistics'], lower_cs_count)
    write_type_unit_count('CSVs/gradReqsLOWER.csv', 'CSVs/gradReqsLowerMATH', math_matches, sci_matches + ['Discrete'], lower_math_count)
    write_type_unit_count('CSVs/gradReqsLOWER.csv', 'CSVs/gradReqsLowerSCI' , sci_matches , [], lower_sci_count)
    write_type_unit_count('CSVs/gradReqsLOWER.csv', 'CSVs/gradReqsLowerOTHER', ['PHIL ', 'ENGL '], cs_matches + math_matches + sci_matches, lower_other_count)

    upper_cs_count = {}
    upper_math_count = {}
    upper_sci_count = {}
    upper_other_count = {}
    write_type_unit_count('CSVs/gradReqsUPPER.csv', 'CSVs/gradReqsUpperCS'  , cs_matches  , ['Statistics', 'Probability'], upper_cs_count)
    write_type_unit_count('CSVs/gradReqsUPPER.csv', 'CSVs/gradReqsUpperMATH', math_matches, ['Discrete'], upper_math_count)
    write_type_unit_count('CSVs/gradReqsUPPER.csv', 'CSVs/gradReqsUpperSCI' , sci_matches , [], upper_sci_count)
    write_type_unit_count('CSVs/gradReqsUPPER.csv', 'CSVs/gradReqsUpperOTHER', ['PHIL ', 'ENGL ', 'ES/WGQS '], cs_matches + math_matches + sci_matches, upper_other_count)

    total_count = {}
    grand_total = 0
    for school in lower_count:
        total_count[school] = lower_count[school] + upper_count[school]
        if "UC" in school or "San Luis Obispo" in school:
            if "Berkeley" not in school and "Merced" not in school:
                total_count[school] /= 1.5
        grand_total += total_count[school]

    highest = max(total_count, key=total_count.get)
    lowest = min(total_count, key=total_count.get)

    print("Mean of semester units: " + str(grand_total/len(total_count)))
    print("Highest unit count: ", highest)
    print("Lowest unit count: ", lowest)
    '''
