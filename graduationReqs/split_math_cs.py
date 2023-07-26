import csv

def write_csv(csv_path, name, matches):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        if '.csv' not in name[-4:]:
            name += '.csv'
        
        with open(name, 'w') as new_file:
            csv_writer = csv.writer(new_file)

            for line in csv_reader:
                if any([x in line[1] for x in matches]):
                    csv_writer.writerow(line)

if __name__ == '__main__':
    path = input('Enter CSV file path: ')
    cs_name = input('Enter desired name for CS CSV file: ')
    math_name = input('Enter desired name for math CSV file: ')

    cs_matches = ['CS', 'CSE', 'ECS', 'EEC', 'I&C', 'IN4MATX', 'COM SCI', 'CMPSC', 'CPSC', 'COMP', 'CSCI', 'CSC', 'CECS', 'CMPS', 'CST', 'ENGR', 'ECE']
    math_matches = ['Math ', 'MATH ', 'MAT ', 'STAT', 'Statistics', 'Probability & Stat', 'Probability and Stat', 'Statistics & Probability', 'Statistics and Probability', 'Discrete']
    # PSTAT STA STAT STATS
    write_csv(path, cs_name, cs_matches)
    write_csv(path, math_name, math_matches)
