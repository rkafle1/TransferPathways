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
    # if "No Course Articulated" in str:
    #     return True
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
#------------------------------------------------------------------------------------------------------------------------------------------------------   

# SDSU
def getCoursesSDSU(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if "PREPARATION FOR THE MAJOR" in splitlist[i]:
            start = i + 1
            break
    for i in range(start, len(splitlist)):
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ':
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' '))
    return Courses

def DictFromTxtSDSU(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesSDSU(reqdict, RequiredClasses)
    # print(RequiredClasses)
    for i in range(len(RequiredClasses)):
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')
        if '←' in RequiredClasses[i]:
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue
       
        
        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    
                    if j not in reqqueue:

                        reqqueue.append(j)
                    continue
        
        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
               
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
    for i in reqqueue:
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
    
#-------------------------------------------------------------------------------------------------------------------------------------------------
# CSUSM
def getCoursesCSUSM(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'Courses section*' in splitlist[i]:
            start = i + 1
            break
    for i in range(start, len(splitlist) - 1):
        # if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict)) and ".00" in splitlist[i + 1][(len(splitlist)-4):] and len(splitlist[i + 1]) == 6:
        #     units = splitlist[i + 1]
        #     splitlist[i] = splitlist[i] + units
        #     splitlist[i + 1] = ''
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
            print("has an arrow not first")
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ':
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        
        
    print(Courses)
    return Courses

def DictFromTxtCSUSM(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUSM(reqdict, RequiredClasses)
    # print(RequiredClasses)
    for i in range(len(RequiredClasses)):
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    # print(RequiredClasses[i] + " is a required class")
                    if j not in reqqueue:

                        reqqueue.append(j)
                    continue
        
        if '←' in RequiredClasses[i]:
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue
       
        
        
        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1]:
               
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            # if "--- And ---" in RequiredClasses[i + 1]:
            #     index = len(artqueue[len(artqueue) - 1]) - 1
            #     artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
            #     continue
    for i in reqqueue:
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
        if "BIOL 160 - Microbiology for Health Sciences (4.00)" in i:
            break
    return Articulations
# ------------------------------------------------------------------------------------------------------------------------------------------------

# CSULB
def getCoursesCSULB(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if "CECS\u200b 105 - \u200bIntroduction to Computer Engineering and Computer" in splitlist[i]:
            print("found the first case")
            start = i 
            break
    if start == 0:
        print("start is the first")
    for i in range(start, len(splitlist) - 1):
        # if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict)) and ".00" in splitlist[i + 1][(len(splitlist)-4):] and len(splitlist[i + 1]) == 6:
        #     units = splitlist[i + 1]
        #     splitlist[i] = splitlist[i] + units
        #     splitlist[i + 1] = ''
        if ".00" in splitlist[i + 1] and '\u200b' not in splitlist[i + 1]:
            # add i + 1 to the ith string and replace i + 1 with an empty string
            splitlist[i] = splitlist[i] + " " + splitlist[i + 1]
            splitlist[i + 1] = ""
        if "←" in splitlist[i] and "←" != splitlist[i][0]:
            print("has an arrow not first")
            for x in range(len(splitlist[i])):
                if splitlist[i][x] == "←":
                    splitlist.insert(i+1, splitlist[i][x:])
                    splitlist[i] = splitlist[i][:x]
                    break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ':
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        
        
   
    return Courses

def DictFromTxtCSULB(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSULB(reqdict, RequiredClasses)
    
    arrowcnt = 0
    for i in range(len(RequiredClasses)):
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    # print(RequiredClasses[i] + " is a required class")
                    if j not in reqqueue:

                        reqqueue.append(j)
                    continue
        
        if '←' in RequiredClasses[i]:
            arrowcnt += 1
            if arrowcnt == 1:
                artqueue.insert(1, [[RequiredClasses[i].replace('← ', '')]])
            elif arrowcnt == 2:
                artqueue.insert(2, [[RequiredClasses[i].replace('← ', '')]])
            elif arrowcnt == 3:
                artqueue.insert(0, [[RequiredClasses[i].replace('← ', '')]])
            else:
                artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue
       
        
        
        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] :
               
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            # if "--- And ---" in RequiredClasses[i + 1]:
            #     index = len(artqueue[len(artqueue) - 1]) - 1
            #     artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
            #     continue
    for i in reqqueue:
        if i in reqdict["APPROVED SCIENCES ELECTIVES (MINIMUM OF EIGHT UNITS), TAKE:"]:
            break
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
# -------------------------------------------------------------------------------------------------------------------------------------------------

#CSUB
def getCoursesCSUB(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CMPS\u200b 2010 - \u200bProgramming I: Programming Fundamentals (4.00)' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    for i in range(start, len(splitlist) - 1):
        if "CONCENTRATION IN COMPUTER INFORMATION SYSTEMS" in splitlist[i]:
            break
        # if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict)) and ".00" in splitlist[i + 1][(len(splitlist)-4):] and len(splitlist[i + 1]) == 6:
        #     units = splitlist[i + 1]
        #     splitlist[i] = splitlist[i] + units
        #     splitlist[i + 1] = ''
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
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' and "MAJOR IN COMPUTER SCIENCE" not in splitlist[i]:
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        
        
   
    return Courses

def DictFromTxtCSUB(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUB(reqdict, RequiredClasses)
    print(RequiredClasses)
    arrowcnt = 0
    for i in range(len(RequiredClasses)):
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    isReq = True
                    # print(RequiredClasses[i] + " is a required class")
                    if j not in reqqueue:

                        reqqueue.append(j)
                    break
        if isReq:
            continue
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue
       
        
        
        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] :
                if len(artqueue) == 0:
                    print("artqueue is zero", RequiredClasses[i])
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            # if "--- And ---" in RequiredClasses[i + 1]:
            #     index = len(artqueue[len(artqueue) - 1]) - 1
            #     artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
            #     continue
    for i in reqqueue:
        
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
# -----------------------------------------------------------------------------------------------------------------------------------------------
# CSUCI
def getCoursesCSUCI(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'COMP\u200b 162 - \u200bComputer Architecture and Assembly Language (3.00)' in splitlist[i]:
            print("found the first case")
            start = i 
            break
    for i in range(start, len(splitlist) - 1):
        
        # if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict)) and ".00" in splitlist[i + 1][(len(splitlist)-4):] and len(splitlist[i + 1]) == 6:
        #     units = splitlist[i + 1]
        #     splitlist[i] = splitlist[i] + units
        #     splitlist[i + 1] = ''
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
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' and "MAJOR IN COMPUTER SCIENCE" not in splitlist[i]:
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        
        
   
    return Courses

def DictFromTxtCSUCI(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUCI(reqdict, RequiredClasses)
    print(RequiredClasses)
    arrowcnt = 0
    for i in range(len(RequiredClasses)):
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                   
                    # print(RequiredClasses[i] + " is a required class")
                    if j not in reqqueue:

                        reqqueue.append(j)
                    continue
        
        if '←' in RequiredClasses[i]:
            
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue
       
        
        
        # handle case of it is an articulation that goes with another ariticulation in artqueue
        # artqueue: [ [(req1)[opt 1], [opt 2], ]]
        if isArticulation(RequiredClasses[i]) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] :
               
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            # if "--- And ---" in RequiredClasses[i + 1]:
            #     index = len(artqueue[len(artqueue) - 1]) - 1
            #     artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
            #     continue
    for i in reqqueue:
        # print(i, CCName, artqueue)
        if len(artqueue) == 0:
            Articulations[reqToString(i)] = [["this and anything after this is incorrect"]]
            break
        if "MATH 300 - Discrete Mathematics (3.00)" in i:
            Articulations[reqToString(i)] = artqueue[len(artqueue) - 1]
            break
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
# -----------------------------------------------------------------------------------------------------------------------------------------
# CSUF
def getCoursesCSUF(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CPSC\u200b 120 - \u200bIntroduction to Programming (3.00)' in splitlist[i]:
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
        if 'MATH AND SCIENCE (WITH CORRESPONDING LAB) ELECTIVES- SEE ADDITIONAL INFORMATION UNDER' in splitlist[i]:
            for j in range(i, len(splitlist)):
                if '\x0cARTICULATION DETAILS' in splitlist[j]:
                    i = j
                    break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' and "MAJOR IN COMPUTER SCIENCE" not in splitlist[i]:
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1
        
        
   
    return Courses

def DictFromTxtCSUF(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUF(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    
                    # print(RequiredClasses[i] + " is a required class")
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
            if "--- Or ---" in RequiredClasses[i - 1] :
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
    for i in reqqueue:
        if "MATH 300 - Discrete Mathematics (3.00)" in i:
            Articulations[reqToString(i)] = artqueue[len(artqueue) - 1]
            break
        if "CHEM 120A - General Chemistry (5.00)" in i:
            break
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
# -------------------------------------------------------------------------------------------------------------------
# CSULA
def getCoursesCSULA(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CS\u200b 1222 - \u200bIntroduction to Relational Databases (3.00)' in splitlist[i]:
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
        if 'DIVERSITY COURSES FOR CAL STATE LA GRADUATION REQUIREMENT' in splitlist[i]:
            
            break
        if 'LOWER DIVISION REQUIRED COURSES' in splitlist[i] or ' Minimum grade required: C or better ' in splitlist[i]:
            i += 1
            continue
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1
    Courses.append("END OF AGREEMENT")
        
        
   
    return Courses

def DictFromTxtCSULA(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSULA(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    
                    # print(RequiredClasses[i] + " is a required class")
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
            if "--- Or ---" in RequiredClasses[i - 1] :
                if len(artqueue) == 0: 
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
    for i in reqqueue:
        if "MATH 300 - Discrete Mathematics (3.00)" in i:
            Articulations[reqToString(i)] = artqueue[len(artqueue) - 1]
            break
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
#-------------------------------------------------------------------------------------------------
#CSUSB
def getCoursesCSUSB(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSE\u200b 2010 - \u200bComputer Science I (4.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1
        
        
   
    return Courses

def DictFromTxtCSUSB(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUSB(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'PHYSICS REQUIREMENT' in RequiredClasses[i] or ' Series for series only' in RequiredClasses[i] or' Complete entire sequence at' in RequiredClasses[i] or 'transfer' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    
                    # print(RequiredClasses[i] + " is a required class")
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
            if "--- Or ---" in RequiredClasses[i - 1] :
               
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
    for i in reqqueue:
        if "MATH 300 - Discrete Mathematics (3.00)" in i:
            Articulations[reqToString(i)] = artqueue[len(artqueue) - 1]
            break
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
#-----------------------------------------------------------------------------------------------------
# CPP
def getCoursesCPP(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if '\x0cBIO\u200b 1110 - \u200bLife Science (2.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1
        
        
   
    return Courses

def DictFromTxtCPP(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCPP(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIRED: COMPUTER SCIENCE LOWER-DIVISION SEQUENCE' in RequiredClasses[i] or 'MAJOR REQUIRED: CALCULUS-BASED PHYSICS' in RequiredClasses[i] or'MAJOR REQUIRED ELECTIVES' in RequiredClasses[i] or 'transfer' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    
                    # print(RequiredClasses[i] + " is a required class")
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
            if "--- Or ---" in RequiredClasses[i - 1] :
               
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
    for i in reqqueue:
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
    
# -----------------------------------------------------------------------------------------------------
# CSUDH
def getCoursesCSUDH(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSC\u200b 121 - \u200bIntroduction to Computer Science and Programming I' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1
        
        
   
    return Courses

def DictFromTxtCSUDH(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUDH(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIRED: COMPUTER SCIENCE LOWER-DIVISION SEQUENCE' in RequiredClasses[i] or 'MAJOR REQUIRED: CALCULUS-BASED PHYSICS' in RequiredClasses[i] or'MAJOR REQUIRED ELECTIVES' in RequiredClasses[i] or 'transfer' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    
                    # print(RequiredClasses[i] + " is a required class")
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
            if "--- Or ---" in RequiredClasses[i - 1] :
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
    for i in reqqueue:
        if "MATH 300 - Discrete Mathematics (3.00)" in i:
            Articulations[reqToString(i)] = artqueue[len(artqueue) - 1]
            break
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
    
#-----------------------------------------------------------------------------------------------------
# CSUEB
def getCoursesCSUEB(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CS\u200b 101 - \u200bComputer Science I (4.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1
        
        
   
    return Courses

def DictFromTxtCSUEB(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUEB(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIRED: COMPUTER SCIENCE LOWER-DIVISION SEQUENCE' in RequiredClasses[i] or 'LOWER DIVISION CORE' in RequiredClasses[i] or'MAJOR REQUIRED ELECTIVES' in RequiredClasses[i] or 'transfer' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    
                    # print(RequiredClasses[i] + " is a required class")
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
            if "--- Or ---" in RequiredClasses[i - 1] :
               
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
    for i in reqqueue:
        if len(artqueue) == 0:
            artqueue.append([["Fix this manually"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
#------------------------------------------------------------------------------------------------------------------
# CSUFres
def getCoursesCSUFres(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSCI\u200b 40 - \u200bIntroduction to Programming and Problem Solving (4.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1

    return Courses

def DictFromTxtCSUFres(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUFres(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or ' Content credit only' in RequiredClasses[i] or' No upper division credit' in RequiredClasses[i] or  'OTHER DEGREE REQUIREMENTS' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    
                    # print(RequiredClasses[i] + " is a required class")
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
            if "--- Or ---" in RequiredClasses[i - 1] :
               
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
#------------------------------------------------------------------------------------------------------------------------
# Humb
def getCoursesHumboldt(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'MATH\u200b 102 - \u200bAlgebra & Elementary Functions (4.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1

    return Courses

def DictFromTxtHumboldt(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesHumboldt(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or 'ADDITIONAL APPROVED COURSES FOR THE MAJOR' in RequiredClasses[i] or' Only lower division courses listed ' in RequiredClasses[i] or ' **REFER TO TOP OF AGREEMENT** ' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    
                    # print(RequiredClasses[i] + " is a required class")
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
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
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
#------------------------------------------------------------------------------------------------------
# CPSLO
def getCoursesCPSLO(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSC\u200b 101 - \u200bFundamentals of Computer Science (4.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if 'OTHER COURSES (CONCENTRATION/EMPHASIS/ELECTIVES)' in splitlist[i]:
            break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtCPSLO(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCPSLO(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        seen = 0
        # if "BIO 213 - Life Science for Engineers (2.00)" in RequiredClasses[i]:
        #     reqqueue.append(reqdict[""])
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or ' Preferred course' in RequiredClasses[i] or ' Acceptable substitute' in RequiredClasses[i] or ' **REFER TO TOP OF AGREEMENT** ' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            
            
            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    seen += 1
                    
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
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if i in reqdict["select 4 units"]:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
#-----------------------------------------------------------------------------------------------------------------------------------
# CSUMB
def getCoursesCSUMB(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CST\u200b 231 - \u200bProblem Solving and Programming (4.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if 'OTHER COURSES (CONCENTRATION/EMPHASIS/ELECTIVES)' in splitlist[i]:
            break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtCSUMB(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUMB(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        seen = 0
        # if "BIO 213 - Life Science for Engineers (2.00)" in RequiredClasses[i]:
        #     reqqueue.append(reqdict[""])
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or ' Preferred course' in RequiredClasses[i] or ' Acceptable substitute' in RequiredClasses[i] or ' **REFER TO TOP OF AGREEMENT** ' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            
            
            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    seen += 1
                    
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
#-------------------------------------------------------------------------------------------------------
# CSUN
def getCoursesCSUN(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if '← CSCI\u200b 112 - \u200bProgramming Fundamentals I (4.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if 'OTHER COURSES (CONCENTRATION/EMPHASIS/ELECTIVES)' in splitlist[i]:
            break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtCSUN(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUN(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
        seen = 0
        # if "BIO 213 - Life Science for Engineers (2.00)" in RequiredClasses[i]:
        #     reqqueue.append(reqdict[""])
        isReq = False
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or ' Preferred course' in RequiredClasses[i] or ' Acceptable substitute' in RequiredClasses[i] or ' **REFER TO TOP OF AGREEMENT** ' in RequiredClasses[i]:
            continue
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')

        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            
            
            for j in reqdict[key]:
                
                if RequiredClasses[i] in j:
                    seen += 1
                    
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
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
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
#----------------------------------------------------------------------------------------
#CSUS
def getCoursesCSUS(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSC\u200b 15 - \u200bProgramming Concepts and Methodology I (3.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if 'OTHER COURSES (CONCENTRATION/EMPHASIS/ELECTIVES)' in splitlist[i]:
            break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtCSUS(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUS(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or ' Preferred course' in RequiredClasses[i] or ' Acceptable substitute' in RequiredClasses[i] or ' **REFER TO TOP OF AGREEMENT** ' in RequiredClasses[i]:
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
            if "--- And ---" in RequiredClasses[i - 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if "--- And ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if "BIO 10 - Basic Biological Concepts (3.00)" in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations
# ----------------------------------------------------------------------------------------------
# CSUStan
def getCoursesCSUStan(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CS\u200b 1500 - \u200bComputer Programming I (3.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if 'OTHER COURSES (CONCENTRATION/EMPHASIS/ELECTIVES)' in splitlist[i]:
            break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtCSUStan(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesCSUStan(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or ' Preferred course' in RequiredClasses[i] or 'CHOOSE ANY ONE OF THE FOLLOWING SEQUENCES:' in RequiredClasses[i] or ' Series for series only' in RequiredClasses[i]:
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
            if "--- Or ---" in RequiredClasses[i - 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if "BIO 10 - Basic Biological Concepts (3.00)" in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
        if "PHYS 2260 - General Physics II (4.00)" in i:
            break
    return Articulations
# ----------------------------------------------------------------------------------------------------------------------------
# SFSU
def getCoursesSFSU(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSC\u200b 210 - \u200bIntroduction to Computer Programming (3.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if 'OTHER COURSES (CONCENTRATION/EMPHASIS/ELECTIVES)' in splitlist[i]:
            break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtSFSU(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesSFSU(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or ' Preferred course' in RequiredClasses[i] or 'CHOOSE ANY ONE OF THE FOLLOWING SEQUENCES:' in RequiredClasses[i] or ' Series for series only' in RequiredClasses[i]:
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
            if "--- Or ---" in RequiredClasses[i - 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
            if "--- And ---" in RequiredClasses[i - 1]:
                if len(artqueue) == 0:
                    continue
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
                continue
            
            if '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
                continue
    for i in reqqueue:
        if "BIO 10 - Basic Biological Concepts (3.00)" in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
        if "PHYS 2260 - General Physics II (4.00)" in i:
            break
    return Articulations
def getCoursesSJSU(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'ENGL\u200b 1B - \u200bArgument and Analysis (3.00)' in splitlist[i]:
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
        
        if 'LOWER DIVISION REQUIREMENTS' in splitlist[i]:
            i += 1
            continue
        if 'OTHER COURSES (CONCENTRATION/EMPHASIS/ELECTIVES)' in splitlist[i]:
            break
        if (isArticulation(splitlist[i]) or isReqCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) and splitlist[i] != ' ' :
            Courses.append(splitlist[i].replace('\u200b', ' ').replace('  ', ' ').replace('\x0c', ''))
        i += 1  
    Courses.append("END OF AGREEMENT")
    return Courses

def DictFromTxtSJSU(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesSJSU(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or ' Preferred course' in RequiredClasses[i] or 'CHOOSE ANY ONE OF THE FOLLOWING SEQUENCES:' in RequiredClasses[i] or ' Series for series only' in RequiredClasses[i]:
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
        if "BIO 10 - Basic Biological Concepts (3.00)" in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
        if "PHYS 2260 - General Physics II (4.00)" in i:
            break
    return Articulations
def getCoursesSonoma(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CS\u200b 115 - \u200bProgramming I (4.00)' in splitlist[i]:
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

def DictFromTxtSonoma(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesSonoma(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or ' Preferred course' in RequiredClasses[i] or '           ' not in RequiredClasses[i] or ' Series for series only' in RequiredClasses[i]:
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
        if "BIO 10 - Basic Biological Concepts (3.00)" in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
        if "PHYS 2260 - General Physics II (4.00)" in i:
            break
    return Articulations
def getCoursesChico(reqdict, splitlist):

    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if 'CSCI\u200b 111 - \u200bProgramming and Algorithms I (4.00)' in splitlist[i]:
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

def DictFromTxtChico(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCoursesChico(reqdict, RequiredClasses)
    print(RequiredClasses)
    
    for i in range(len(RequiredClasses)):
       
        isReq = False
        
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break

        if 'MAJOR REQUIREMENTS' in RequiredClasses[i] or 'LOWER DIVISION' in RequiredClasses[i] or ' Preferred course' in RequiredClasses[i] or 'SUPPORT COURSES' in RequiredClasses[i] or ' Series for series only' in RequiredClasses[i]:
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
        if "BIO 10 - Basic Biological Concepts (3.00)" in i:
            break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        if ['CHEM 111 - General Chemistry I (4.00)'] in artqueue[0]:
            Articulations[reqToString(i)] = [artqueue[0][0]]
            break
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
        if "PHYS 2260 - General Physics II (4.00)" in i:
            break
    return Articulations