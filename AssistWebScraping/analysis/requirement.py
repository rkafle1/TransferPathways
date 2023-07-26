# college name, list of requirements, list of articulations
# Evergreen vallye... , [['8A...', '8b...'], ['cs 11']], "[[[8asart(classa, classb)]], [[8bsart]], [[11s]]]"

# Essentially, col b(arrow reqs) are in a list following the and or relationships on the agreement and articulations are taken directly from their rows in the og csvs
# and listed in order of the requirement courses

# from ProcessFile import *
from Requirements import *
# import sys
# #absolute path for the assist web scraping folder
# sys.path.insert(1, 'C:/Users/a2576/Documents/GitHub/TransferPathways/AssistWebScraping/analysis')

from AssistAPIInformationGetter import *
# from writeToCSV import *
import statistics
import pandas as pd
import numpy as np
import math

import re
import ast

df = pd.read_csv("./UCIGradreqs.csv", header=None, sep='\t')
row, column = df.shape
print(row, column)
print(df.iloc[0,1])
print(df.iloc[0,2])
dict = {}

nolist =    ['No Course Articulated', 
            'This course must be taken at the university after transfer',
            'Course(s) Denied', 
            'Not Articulated',
            'No Comparable Course',
            'No Articulation Established',
            'Articulates as Course-to-Course Only',
            'Articulates as a Series Only',
            'Articulation Pending Review',
            'No Current Articulation' 
        ]
def join_with_or(lst):
    return " or ".join(lst)

def convert_to_numerical(data):
    count = 1
    def get_numeric_value(item):
        nonlocal count
        if isinstance(item, list):
            return [get_numeric_value(sub_item) for sub_item in item]
        else:
            count_str = str(count)
            count += 1
            return count_str
    return get_numeric_value(data)

def convert_to_boolean(data):
    def get_boolean_value(item):
        # print(item)
        if isinstance(item, list):
            return [get_boolean_value(sub_item) for sub_item in item]
        else:
            return str(item not in nolist)
    return get_boolean_value(data)


def convert_to_logical_expression(data):
    sub_expressions = []
    for index, item in enumerate(data):
        # print(index, item)
        if isinstance(item, list):
            sub_expression = "(" + join_with_or(item) + ")"
        else:
            sub_expression = str(item)
        sub_expressions.append(sub_expression)

    return " and ".join(sub_expressions)


def substitute_with_bool(expression, bool_list):
    # Convert the boolean values to their corresponding string representations
    bool_str_list = [str(val) for val in bool_list]

    # Use regular expression to find all the numbers in the expression
    numbers = re.findall(r'\d+', expression)

    # Replace each number with the corresponding boolean value from the bool_list
    for i in range(len(numbers)):
        num = int(numbers[i])
        if 1 <= num <= len(bool_list):
            expression = expression.replace(numbers[i], bool_str_list[num - 1], 1)

    return expression


# logical_exp = convert_to_logical_expression(convert_to_numerical(ast.literal_eval(df.iloc[0,1])))
# print(logical_exp)

# booleanlists = []
# for item in (ast.literal_eval(df.iloc[0,2])):
#     exp = convert_to_logical_expression(convert_to_boolean(item))
#     print(eval(exp))
#     booleanlists.append(eval(exp))

# print(logical_exp)
# print(booleanlists)
# finalans = substitute_with_bool(logical_exp, booleanlists)
# print(eval(finalans))





print("row", row)
for i in range(row):
    ccName = df.iloc[i,0]
    courseName = df.iloc[i,1]
    logical_exp = convert_to_logical_expression(convert_to_numerical(ast.literal_eval(courseName)))
    print(logical_exp)
    articulationName = df.iloc[i,2]
    booleanlists = []
    for item in (ast.literal_eval(articulationName)):
        exp = convert_to_logical_expression(convert_to_boolean(item))
        # print(eval(exp))
        booleanlists.append(eval(exp))
    finalans = substitute_with_bool(logical_exp, booleanlists)
    # print(eval(finalans))

    if(ccName is np.nan):
        continue
    else:
        if(ccName not in list(dict.keys())):
            dict[ccName]= 0
            if eval(finalans) == True:
                print(ccName, "requirement met", " in line ", 2*i+1 )
                dict[ccName]+= 1
            firstone = True
        else:
            if eval(finalans) == True:
                print(ccName, "requirement met", " in line ", 2*i-1 )
                dict[ccName]+= 1
print(dict)



# def requirementmet(a, b):
#     for i in range(row):
#         #skip if it is empty
#         element = df.iloc[i,2]
#         if(element is np.nan):
#             continue
#         else:
           

# iterate(df, row)