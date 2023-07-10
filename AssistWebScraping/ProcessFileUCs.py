from pdfminer.high_level import extract_text
from AssistAPIInformationGetter import *
# checks if a string contains a course or somthing needed to link requirements
def isCourse(str):
    if str == '' or str == ' ':
        return False
    if "MAJOR PREPARATION COURSES REQUIRED FOR TRANSFER" in str:
        return False
    return True

# decides if a string is an articulation course
def isArticulation(str):
    if "--- And ---" in str or "--- Or ---" in str:
        return False
    if "One additional approved transferable course for the major" in str or "approved Math, Science, or CSE course):" in str:
        return False
    if "Please refer to additional important General Information" in str or  "section above" in str or str in "(4.00)":
        return False
    if "PREPARATION FOR THE MAJOR" in str or "Same-As" in str or "All courses in this section are required" in str or 'from the following' in str:
        return False
    if "    " in str:
        return False
    # if isReqCourse(str, reqdict):
    #     return False
    return True
# checks if a string should be added to Requiredclasses
def isvalidstr(str):
    if isArticulation(str) or str in "--- And ---" or str in "--- Or ---":
        return True
    return False

# checks if a str is a university required course
def isReqCourse(str, reqdict):
    for key in reqdict.keys():
        for i in reqdict[key]:
            if str in i:
                return True
    return False

def reqToString(lst):
    str = ""
    for i in lst:
        str = str + i + " & "
    return str[:len(str) - 3]



# UCI
def getCoursesUCI(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'I&C SCI\u200b 31 - \u200bIntroduction to Programming (4.00)' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    i = start
    while i < len(splitlist) - 1:
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
           
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtUCI(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesUCI(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or 'ONE ADDITIONAL APPROVED TRANSFERABLE COURSE FOR THE MAJOR (MATH OR CS COURSE)' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue

            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    
                    
                    if j not in reqqueue:
                        isReq = True
                        reqqueue.append(j)
                        break 
            if isReq:
                break
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue

        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if 'I&C SCI 6N - Computational Linear Algebra (4.00)' in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations

# ------------------------------------------------------------------------------------------------------------------------------------------------   

# UCD

def getCoursesUCD(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if '\x0cECS\u200b 020 - \u200bDiscrete Mathematics For Computer Science (4.00)' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    i = start
    while i < len(splitlist) - 1:
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
           
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtUCD(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesUCD(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or 'ADDITIONAL MAJOR PREPARATION COURSES' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue

            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    
                    
                    if j not in reqqueue:
                        isReq = True
                        reqqueue.append(j)
                        break 
            if isReq:
                break
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue

        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if i in reqdict["select 1 course"][1:]:
            artqueue.remove(artqueue[0])
            continue
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations

#------------------------------------------------------------------------------------------------------------------------------------------------------   
# UCLA
def getCoursesUCLA(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'MATH\u200b 31A - \u200bDifferential and Integral Calculus (4.00)' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    i = start
    while i < len(splitlist) - 1:
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
           
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtUCLA(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesUCLA(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or 'STRONGLY RECOMMENDED COURSES' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue

            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    
                    
                    if j not in reqqueue:
                        isReq = True
                        reqqueue.append(j)
                        break 
            if isReq:
                break
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue

        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
      
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
# ----------------------------------------------------------------------------------------
# UCR
def getCoursesUCR(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CS\u200b 10A - \u200bIntro to Computer Science for Science, Mathematics' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    i = start
    while i < len(splitlist) - 1:
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
           
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtUCR(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesUCR(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or 'STRONGLY RECOMMENDED COURSES' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue

            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    
                    
                    if j not in reqqueue:
                        isReq = True
                        reqqueue.append(j)
                        break 
            if isReq:
                break
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue

        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if "MATH 10A - Calculus ofSeveral Variables (4.00)" in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
# -----------------------------------------------------------------------------------------------
#UCSD
def getCoursesUCSD(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSE\u200b 8A - \u200bIntroduction to Programming and Computational' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    i = start
    while i < len(splitlist) - 1:
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
           
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtUCSD(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesUCSD(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or 'STRONGLY RECOMMENDED COURSES' in RequiredClasses[i] or '               ' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue

            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    
                    
                    if j not in reqqueue:
                        isReq = True
                        reqqueue.append(j)
                        break 
            if isReq:
                break
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue

        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if "MATH 10A - Calculus ofSeveral Variables (4.00)" in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations

#------------------------------------------------------------------------------------
# UCB
def getCoursesUCB(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'COMPSCI\u200b 61A - \u200bThe Structure and Interpretation of Computer Programs' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    i = start
    while i < len(splitlist) - 1:
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
           
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtUCB(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesUCB(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or 'STRONGLY RECOMMENDED COURSES' in RequiredClasses[i] or '               ' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue

            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    
                    
                    if j not in reqqueue:
                        isReq = True
                        reqqueue.append(j)
                        break 
            if isReq:
                break
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue

        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if "MATH 10A - Calculus ofSeveral Variables (4.00)" in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations


# UCSC
def getCoursesUCSC(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSE\u200b 30 - \u200bProgramming Abstractions: Python (7.00)' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    i = start
    while i < len(splitlist) - 1:
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
           
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtUCSC(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesUCSC(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'STRONGLY RECOMMENDED ADVANCED PREPARATION COURSES' in RequiredClasses[i] or 'STRONGLY RECOMMENDED COURSES' in RequiredClasses[i] or 'MAJOR PREPARATION COURSES' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue

            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    
                    
                    if j not in reqqueue:
                        isReq = True
                        reqqueue.append(j)
                        break 
            if isReq:
                break
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue

        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations


def getCoursesUCSB(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if '\x0cMATH\u200b 3A - \u200bCalculus with Applications, First Course (4.00)' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    i = start
    while i < len(splitlist) - 1:
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
           
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtUCSB(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesUCSB(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'STRONGLY RECOMMENDED ADVANCED PREPARATION COURSES' in RequiredClasses[i] or 'STRONGLY RECOMMENDED COURSES' in RequiredClasses[i] or 'MAJOR PREPARATION COURSES' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue

            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    
                    
                    if j not in reqqueue:
                        isReq = True
                        reqqueue.append(j)
                        break 
            if isReq:
                break
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue

        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations




def getCoursesUCM(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSE\u200b 020 - \u200bIntroduction to Computing I (2.00)' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    i = start
    while i < len(splitlist) - 1:
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
           
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtUCM(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesUCM(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'STRONGLY RECOMMENDED' in RequiredClasses[i] or 'ACADEMIC WRITING - CHOOSE ONE COURSE FROM:' in RequiredClasses[i] or ' Effective next fall' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue

            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    
                    
                    if j not in reqqueue:
                        isReq = True
                        reqqueue.append(j)
                        break 
            if isReq:
                break
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue

        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if "MATH 032 - Probability and Statistics (4.00)" in i:
            Articulations[reqToString(i)] = artqueue[5]
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations