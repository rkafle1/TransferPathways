# from ProcessFile import *
from Requirements import *
import ProcessFile
from AssistAPIInformationGetter import *
from writeToCSV import *
import statistics
import pandas as pd
import numpy as np
import math
import re
import ast



#checks the validity of an input element based on matching pairs of characters (parentheses, brackets, quotes) using the pairs dictionary.
#return true/false, and the error message
def isValid(element):
    #if element has matching ones
    pairs = {
            ")": "(",
            "]": "[",
            "b": "a", #single quotes, b is the second quote, a is the first quote
            "d": "c"  #double quotes, d is the second quote, c is the first quote
        }
    list1 = ["(", "[", "]", ")" ]
    #only store the characters that are in the pairs dictionary, delete the ones that are not in the pairs dictionary
    s = ""
    countsingle = 0
    countdouble = 0
    for ch in element:
        if ch in list1:
            s += ch
        elif ch == "'":
            countsingle += 1    
            if(countsingle % 2 == 1):
                s += "a" 
            elif (countsingle % 2 == 0):
                s += "b"
        elif ch == "\"":
            countdouble += 1
            if(countdouble % 2 == 1):
                s += "c"
            elif (countdouble % 2 == 0):
                s += "d"    
    #simple check if it has matching quotes
    if(((s.count("a") + s.count("b")) % 2 != 0) or ((s.count("c") + s.count("d")) % 2 != 0)):
        #There might be situations where there is a single quote insite double quotes, eg."Intro to Biology's scientific method"
        #Therefore, we need to manually check if it is the case or it is the quote missmatching
        return (False, s + " has no matching quotes(might have both quotes at the same time, need to validate)")

    
    #if element has matching pair in pairs, the stack is used to keep track of opening characters (like '(', '[', 'a', 'c'),
    # as they need to be matched withclosing characters.
    stack = list()
    for ch in s:
        if ch in pairs:
            # Check if the stack is empty or the top of the stack doesn't match the expected pair
            if not stack or stack[-1] != pairs[ch]:
                return (False, s + " has no matching [] or () or quotes")
            # If the pairs match, pop the corresponding opening character from the stack
            stack.pop()
        else:
            stack.append(ch)
    return (not stack, s + ", has no matching [] or () or quotes")

    
    


def iterate(df, row):
    for i in range(row):
        #skip if it is empty, depends on the csv file, if we have an empty line or not between the classes
        element = df.iloc[i,2]
        if(element is np.nan):
            continue
        else:
            #if it is not empty, then check if it is valid
            # print(type(df.iloc[i,2]))
            x, y = isValid(element)
            if (x == False):
                print("Not valid on index " + str(i)+ ". The message is " + y)
            #if element has units for a class
            #all possible no articulation cases
            if 'No Course Articulated' not in element\
                and 'This course must be taken at the university after transfer' not in element \
                and 'Course(s) Denied' not in element \
                and 'Not Articulated' not in element \
                and 'No Comparable Course' not in element \
                and 'No Articulation Established' not in element \
                and 'Articulates as Course-to-Course Only' not in element \
                and 'Articulates as a Series Only' not in element \
                and 'Articulation Pending Review' not in element \
                and 'No Current Articulation' not in element:
                #then check if it has units
                try:
                    # Convert the string back into a list of lists
                    courses = ast.literal_eval(element)
                    # Iterate through each course
                    for course_list in courses:
                        for course in course_list:
                            # The regular expression matches a number followed by ".00" surrounded by parentheses at the end of the string
                            # print(i)
                            match = re.search(r'\(\d+\.\d+\)$', course)
                            if match is None:
                                # If the regular expression didn't match, the course doesn't have an associated unit
                                print("Not valid on index " + str(i)+ ". No units for " + course)
                    # If all courses had associated units, return True
                except (ValueError, SyntaxError):
                    # If the string couldn't be converted back into a list of lists, return False
                    print("Try error on index " + str(i), "missing or extra new line")


#CHANGE if needed, change the according csv file path to validate each university
df = pd.read_csv("./csvs/csvs/Assist PDF scraped agreements - SJSU.csv", header=None)
row = df.shape[0]
iterate(df, row)
