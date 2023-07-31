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
import seaborn as sns
import plotly.express as px

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




def GetCountOfMetReqsUni(UniName):
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
#university and dictionary of met requirements
def AllListsofMetReqsCount(UniList):
    fulldic = {}
    with open("csvs/Findings/TotalMetReqsCount.csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for uni in UniList: 
            # print(uni) 
            fulldic[uni] = []
            dictreqs, _ = GetCountOfMetReqsUni(uni)
            # print(dictreqs)
            fulldic[uni] = dictreqs
            writer.writerow([uni, dictreqs])
            dictreqs = []
            print("Done with ", uni , " count")
        return None

#descriptions of count of met requirements
def AllListsofMetReqsCountStats(UniList):
    fulldic = {}
    with open("csvs/Findings/MetReqsCountStats.csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["University", "Total", "max", "min", "median", "mean", "quantiles", "Values"])
        for uni in UniList: 
            # print(uni) 
            fulldic[uni] = []
            dictreqs, totalreq = GetCountOfMetReqsUni(uni)
            # print(dictreqs)
            print("total reqs", totalreq)
            # fulldic["total"] = totalreq

            #analyze the data, get some basic data
            #number of requirements met
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

            writer.writerow([uni, totalreq, max_value, min_value, median_value, mean_value, quantiles, values])
            dictreqs = []
            print("Done with ", uni , " count")
        return fulldic
    
#descriptions of percentage of met requirements
def AllListsofMetReqsPercentageStats(UniList):
    fulldic = {}
    with open("csvs/Findings/MetReqsPercentageStats.csv", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["University", "Total", "max", "min", "median", "mean", "quantiles", "Values"])
        for uni in UniList: 
            # print(uni) 
            fulldic[uni] = []
            dictreqs, totalreq = GetCountOfMetReqsUni(uni)
            # print(dictreqs)
            print("total reqs", totalreq)
            # fulldic["total"] = totalreq

            #analyze the data, get some basic data
            #number of requirements met
            values = list(dictreqs.values())
            values = [value / totalreq for value in values]
            # print("values", values)
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

            writer.writerow([uni, totalreq, max_value, min_value, median_value, mean_value, quantiles, values])
            dictreqs = []
            print("Done with ", uni , " percentage")
        return fulldic

#[,,,,]
def getListOfValues(UniList):
    data = []
    for uni in UniList: 
            # print(uni) 
        dictreqs, totalreq = GetCountOfMetReqsUni(uni)
        values = list(dictreqs.values())
        data.append(values)
    print(data)
    return data

def transform_csv():
    # Read the CSV file into a DataFrame
    df = pd.read_csv("csvs/Findings/MetReqsCountStats.csv", delimiter='\t')

    # Initialize an empty list to store the transformed data
    transformed_data = []

    # Process the data and create the new format
    for row in df.itertuples(index=False):
        key = row[0]
        values = row[7]
        number_list = ast.literal_eval(values)
        for value in number_list:
            # print(value)
            # if value != "," and value != "[" and value != "]" and value != " ":
            transformed_data.append([key, value])

    # Create a new DataFrame with the transformed data
    new_df = pd.DataFrame(transformed_data, columns=['University', 'Values'])

    # Write the new DataFrame to a new CSV file
    new_df.to_csv("csvs/Findings/violin.csv", index=False)

def transform_heatmap():
    # Read the CSV file into a DataFrame
    df = pd.read_csv("csvs/Findings/TotalMetReqsCount.csv", delimiter='\t', header=None)
    print(df.head())
    # Initialize an empty list to store the transformed data
    transformed_data = []

    # Process the data and create the new format
    for row in df.itertuples(index=False):
        key = row[0]
        pairs = row[1]
        for cc, value in ast.literal_eval(pairs).items():
            transformed_data.append([key, cc, value])
        

    # Create a new DataFrame with the transformed data
    new_df = pd.DataFrame(transformed_data, columns=['University', 'CC', 'Values'])

    # Write the new DataFrame to a new CSV file
    new_df.to_csv("csvs/Findings/heatmap.csv", index=False)
# def box_plotting():

#     # df = pd.read_csv(stats_path, header=None, sep='\t')

#     data = getListOfValues(CSVHandling.UniNameShort)
#     fig = plt.figure(figsize =(10, 7))
#     # Creating axes instance
#     ax = fig.add_axes([0, 0, 1, 1])
#     ax = fig.add_subplot(111)

#     bp = ax.boxplot(data)
#     #add the scatter points
#     for i, d in enumerate(data):
#         x = np.random.normal(i + 1, 0.01, size=len(d))  # Spread out the points a bit for better visibility
#         ax.scatter(x, d, alpha=0.3)  # alpha controls the transparency of the scatter points

#     #boxes - interquartile range (IQR)(the middle 50% of the data.) The horizontal line in the box - median, whiskers - 1.5 times the IQR, other points beyond - outliers 
#     plt.title("Boxplot of Met Requirements")
#     plt.xlabel("Universities")
#     # plt.ylabel("Number of Requirements Met")
#     plt.ylabel("Percentage of Requirements Met")
#     plt.xticks(np.arange(1, len(CSVHandling.UniNameShort)+1), CSVHandling.UniNameShort, rotation=45)
#     plt.show()
# # Show the plot



    
#create the csv files for the met requirements
# AllListsofMetReqsCount(CSVHandling.UniNameShort)
# AllListsofMetReqsCountStats(CSVHandling.UniNameShort)
# AllListsofMetReqsPercentageStats(CSVHandling.UniNameShort)
# box_plotting()

Countdf = pd.read_csv("csvs/Findings/MetReqsCountStats.csv", delimiter='\t')
print(Countdf.head())

#visualization of met requirements
# violin graph for count



def graph1():
    figure, axis = plt.subplots(2, 2, figsize=(10, 8))
    sns.violinplot(data=Countdf, x = "Total", ax=axis[0,0])
    axis[0,0].set_title("Total requirements")
    sns.violinplot(data=Countdf, x = "max", ax=axis[0,1])
    axis[0,1].set_title("Max requirements")
    sns.violinplot(data=Countdf, x = "min", ax=axis[1,0])
    axis[1,0].set_title("Min requirements")
    sns.violinplot(data=Countdf, x = "median", ax=axis[1,1])
    axis[1,1].set_title("Median requirements")


# Show the plot
def graph2():
    data = getListOfValues(CSVHandling.UniNameShort)
    figure2 = plt.figure(figsize =(10, 7))
    axis2 = figure2.add_axes([0, 0, 1, 1])
    axis2 = figure2.add_subplot(111)

    bp = axis2.boxplot(data)
    #add the scatter points
    for i, d in enumerate(data):
        x = np.random.normal(i + 1, 0.01, size=len(d))  # Spread out the points a bit for better visibility
        #labels , label=f'University {i+1}' not needed
        axis2.scatter(x, d, alpha=0.3)  # alpha controls the transparency of the scatter points

        #boxes - interquartile range (IQR)(the middle 50% of the data.) The horizontal line in the box - median, whiskers - 1.5 times the IQR, other points beyond - outliers 
        axis2.set_title("Boxplot of Met Requirements")
        axis2.set_xlabel("Universities")
        # plt.ylabel("Number of Requirements Met")
        axis2.set_ylabel("Percentage of Requirements Met")
        axis2.legend()
        axis2.set_xticklabels(CSVHandling.UniNameShort, rotation=45)
 
def graph3():
    transform_csv()
    df3 = pd.read_csv("csvs/Findings/violin.csv")
    print(df3.head())
    print(df3.columns)
    figure3 = plt.figure(figsize=(10, 8))
    axis3 = sns.violinplot(data = df3, x = "University", y = "Values")
    axis3.set_title("Total requirements met Violin plot")
    axis3.set_xlabel("Universities")
    axis3.set_ylabel("Percentage of Requirements Met")
    axis3.set_xticklabels(CSVHandling.UniNameShort, rotation=45)


#px package
    figure4 = px.violin(df3, x="University", y="Values",  points="all", box=True, color="University")
    figure4.show()

    # figure5 = px.strip(df3, x="University", y="Values")
    # figure5.show()
# plt.xticks(rotation=90)
# Show both plots
def heatmap():
    transform_heatmap()
    df = pd.read_csv("csvs/Findings/heatmap.csv", delimiter=',')
    print(df.head())
    print(list(df.columns))
    figure6 = plt.figure(figsize=(10, 8))
    df = df.pivot(index='University', columns='CC', values='Values')
    df = df.reindex(index=CSVHandling.UniNameShort)
    # df = df.reindex(index=CSVHandling.UniNameShort, columns=CSVHandling.CCNameShort)
    axis6 = sns.heatmap(df, cmap="YlOrRd", annot=False, square=False)
    #rainbow YlOrRd YlGnBu
    axis6.set_title("Heatmap of Met Requirements")
    axis6.set_xlabel("Community Colleges")
    axis6.set_ylabel("Universities")
    # axis6.xaxis.tick_top()
    # axis6.set_xticklabels(df['University'].unique(), rotation=45)
    # selected_labels = df['University'].unique()[::2]  # select every second label
    # axis6.set_xticklabels(selected_labels, rotation=45)
    
# graph1()
# graph2()
# graph3()
heatmap()
plt.show()