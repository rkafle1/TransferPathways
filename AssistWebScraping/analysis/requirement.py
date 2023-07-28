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

import csv
import CSVHandling
import matplotlib.pyplot as plt
import statistics

import re
import ast

# df = pd.read_csv("csvs/UniSheets/UCIGradreqs.csv", header=None, sep='\t')
# row, column = df.shape
# print(row, column)
# print(df.iloc[0,1])
# print(df.iloc[0,2])


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




def GetCountOfMetReqsDict(UniName):
    
    dict = {}
    # print(UniName)
    df = pd.read_csv("csvs/UniSheets/"+UniName+"Gradreqs.csv", header=None, sep='\t')
    row, column = df.shape
    print("row", row)
    print("column", column)

    total = 0
    for i in range(row):
        if (df.iloc[i,0] == df.iloc[0,0]):
            total += 1
        else:
            break

    for i in range(row):
        ccName = df.iloc[i,0]
        courseName = df.iloc[i,1]
        logical_exp = convert_to_logical_expression(convert_to_numerical(ast.literal_eval(courseName)))
        # print(logical_exp)
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
                    # print([ccName, courseName])
                    # print(ccName, "requirement met", " in line ", 2*i+1 )
                    dict[ccName]+= 1
            else:
                if eval(finalans) == True:
                    # print([ccName, courseName])
                    # print(ccName, "requirement met", " in line ", 2*i-1 )
                    dict[ccName]+= 1
    return dict, total


# produces dicts of met requirements for all unis and puts it into a csv
def AllListsofMetReqsCount(UniList):
    fulldic = {}
    with open("csvs/Findings/MetReqsCount.csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for uni in UniList: 
            # print(uni) 
            fulldic[uni] = []
            dictreqs, _ = GetCountOfMetReqsDict(uni)
            # print(dictreqs)
            fulldic[uni] = dictreqs
            writer.writerow([uni, dictreqs])
            dictreqs = []
            print("Done with ", uni , " count")

        return None

def AllListsofMetReqsStats(UniList):
    fulldic = {}
    with open("csvs/Findings/MetReqsStats.csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["University", "Total", "max", "min", "median", "mean", "quantiles", "Requirement Values"])
        for uni in UniList: 
            # print(uni) 
            fulldic[uni] = []
            dictreqs, totalreq = GetCountOfMetReqsDict(uni)
            # print(dictreqs)
            print("total reqs", totalreq)
            # fulldic["total"] = totalreq

            #analyze the data, get some basic data
            values = list(dictreqs.values())
            min_value = min(values)
            max_value = max(values)
            median_value = statistics.median(values)
            mean_value = statistics.mean(values)
            # if(len(values) > 4):
            quantiles = np.percentile(values, [25, 50, 75])
            # else:
            #     quantiles = [0,0,0]
            fulldic[uni] = dictreqs
            # writer.writerow([uni, totalreq, max_value, min_value, median_value, mean_value, values])

            writer.writerow([uni, totalreq, min_value, max_value, median_value, mean_value, quantiles, values])
            dictreqs = []
            print("Done with ", uni , " stats")
        return fulldic

def getListOfValues(UniList):
    data = []
    for uni in UniList: 
            # print(uni) 
        dictreqs, totalreq = GetCountOfMetReqsDict(uni)
        values = list(dictreqs.values())
        data.append(values)
    print(data)
    return data

def box_plotting():

    # df = pd.read_csv(stats_path, header=None, sep='\t')

    data = getListOfValues(CSVHandling.UniNameShort)
    fig = plt.figure(figsize =(10, 7))
    # Creating axes instance
    ax = fig.add_axes([0, 0, 1, 1])
    ax = fig.add_subplot(111)

    bp = ax.boxplot(data)
    #add the scatter points
    for i, d in enumerate(data):
        x = np.random.normal(i + 1, 0.01, size=len(d))  # Spread out the points a bit for better visibility
        ax.scatter(x, d, alpha=0.3)  # alpha controls the transparency of the scatter points

    #boxes - interquartile range (IQR)(the middle 50% of the data.) The horizontal line in the box - median, whiskers - 1.5 times the IQR, other points beyond - outliers 
    plt.title("Boxplot of Met Requirements")
    plt.xlabel("Universities")
    plt.ylabel("Number of Requirements Met")
    plt.xticks(np.arange(1, len(CSVHandling.UniNameShort)+1), CSVHandling.UniNameShort, rotation=45)
    plt.show()
# Show the plot



    

# AllListsofMetReqsCount(CSVHandling.UniNameShort)
# AllListsofMetReqsStats(CSVHandling.UniNameShort)
box_plotting()




