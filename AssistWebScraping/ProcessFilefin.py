from pdfminer.high_level import extract_text
from AssistAPIInformationGetter import *
from Requirements import *

# phrases that don't occur in courses
NonCourseWords = ["--- And ---", "--- Or ---", "One additional approved transferable course for the major", "approved Math, Science, or CSE course):", "Please refer to additional important General Information",
                  "section above", "PREPARATION FOR THE MAJOR", "Same-As", "All courses in this section are required", 'from the following', "MAJOR PREPARATION COURSES REQUIRED FOR TRANSFER", "    "]
# Checks if the string is 
def isCourse(str, reqdict):
    if str != '' and str != ' ' and (isArticulation(str, reqdict) or isReqCourse(str, reqdict)):
        return True
    return False

# decides if a string is an articulation course(CC course)
def isArticulation(str, reqdict):
    print(str)
    for word in NonCourseWords:
        if word in str:
            return False 
    if str in "(4.00)" or isReqCourse(str, reqdict):
        return False
    return True
# checks if a string should be added to Requiredclasses
def isvalidstr(str, reqdict):
    if isArticulation(str) or isReqCourse(str, reqdict) or str in "--- And ---" or str in "--- Or ---":
        return True
    return False

# checks if a str is a university required course
def isReqCourse(str, reqdict):
    for key in reqdict.keys():
        for i in reqdict[key]:
            if str in i:
                return True
    return False
# Converts the list of requirement courses to a string
def reqToString(lst):
    str = ""
    for i in lst:
        str = str + i + " & "
    return str[:len(str) - 3]
#------------------------------------------------------------------------------------------------------------------------------------------------------ 
# Shows starts for universities where extract text makes an articulation be the first coursework element
CourseStartexception = {"California State University, Northridge": '← CSCI\u200b 112 - \u200bProgramming Fundamentals I (4.00)'}
StoppingReq = {"California State University, San Marcos": ["BIOL 160 - Microbiology for Health Sciences (4.00)"], "California State University, Channel Islands": ["MATH 300 - Discrete Mathematics (3.00)"], "California State University, Fullerton": ["MATH 300 - Discrete Mathematics (3.00)", "CHEM 120A - General Chemistry (5.00)"], 
               "California State University, Los Angeles": ["MATH 300 - Discrete Mathematics (3.00)"], "California State University, San Bernardino": ["MATH 300 - Discrete Mathematics (3.00)"], "California State University, Sacramento": ["BIO 10 - Basic Biological Concepts (3.00)"], "University of California, Merced": ["MATH 032 - Probability and Statistics (4.00)"]}
# gets the courses into a list
def getCourses(uniname, reqdict, splitlist):
    Courses = []
    start = 0
    for i in range(len(splitlist)):
        if uniname in CourseStartexception.keys() and CourseStartexception[uniname] in splitlist[i]:
            start = i
            break
        else:
            if splitlist[i].replace('\u200b', '').replace('  ', ' ').replace('\x0c', '') in reqdict[list(reqdict.keys())[0]][0]:
                start = i
                break
    for i in range(start, len(splitlist)):
        if (isCourse(splitlist[i], reqdict) or "And" in splitlist[i] or "Or" in splitlist[i]) :
            Courses.append(splitlist[i].replace('\u200b', '').replace('  ', ' ').replace('\x0c', ''))
    return Courses
# puts the mappings of an agreement into a dictionary
# works for all universities except CSULB
def DictFromTxtUnis(uniname, ccname, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    # open the agreement pdf, extract the text, and split the text into a list 
    file = "agreements/report_" + str(getSchoolID(uniname)) +"_" + str(getSchoolID(ccname))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    # get the list of courses from the split text list
    RequiredClasses = getCourses(uniname, reqdict, RequiredClasses)
    # go through each course
    for i in range(len(RequiredClasses)):
        # check that the agreement text we needed is done
        if "END OF AGREEMENT" in RequiredClasses[i]:
            break
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')
        if '←' in RequiredClasses[i]:
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue
        for key in reqdict.keys():
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            for j in reqdict[key]:
                if RequiredClasses[i] in j:
                    if j not in reqqueue:
                        reqqueue.append(j)
                    continue
        
        # handle case of it is an articulation that goes with another ariticulation in artqueue
        if isArticulation(RequiredClasses[i], reqdict) and isReqCourse(RequiredClasses[i], reqdict) == False:
            if "--- Or ---" in RequiredClasses[i - 1] or "--- Or ---" in RequiredClasses[i + 1]:
                if len(artqueue) == 0:
                    continue
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
            elif "--- And ---" in RequiredClasses[i - 1] or "--- And ---" in RequiredClasses[i + 1]:
                index = len(artqueue[len(artqueue) - 1]) - 1
                artqueue[len(artqueue) - 1][index].append(RequiredClasses[i])
            elif '←' == RequiredClasses[i -1][0]:
                artqueue[len(artqueue) - 1].append([RequiredClasses[i]])
    # go through the queues and group the requirement with its articulating courses
    for i in reqqueue:
        if uniname in StoppingReq.keys():
            for req in  StoppingReq[uniname]:
                if req in i:
                    Articulations[reqToString(i)] = artqueue[len(artqueue) - 1]
                    break
        if len(artqueue) == 0:
            artqueue.append([["this needs to be fixed"]])
        Articulations[reqToString(i)] = artqueue[0]
        artqueue.remove(artqueue[0])
    return Articulations

# Scrape the CSULB agreement
def DictFromTxtCSULB(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text(file)
    RequiredClasses = text.split('\n')
    RequiredClasses = getCourses(UniversityName, reqdict, RequiredClasses)
    
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
