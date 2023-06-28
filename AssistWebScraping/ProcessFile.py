from pdfminer.high_level import extract_text

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
    if "No Course Articulated" in str:
        return False
    return True
# checks if a string should be added to Requiredclasses
def isvalidstr(str):
    if isArticulation(str) or str in "--- And ---" or str in "--- Or ---":
        return True
    return False

# checks if a str is a university required course
def isReqCourse(str, reqdict):
    for i in reqdict['cs']:
        if str in i:
            return True
    for i in reqdict['math']:
        if str in i:
            return True
    return False

def reqToString(lst):
    str = ""
    for i in lst:
        str = str + i + " & "
    return str

def getClassTextIrvine(file):
    text = extract_text(file)
    splitByNewln = text.split('\n')
    begin = 0
    for i in range(len(splitByNewln)):
        if "MAJOR PREPARATION COURSES REQUIRED FOR TRANSFER" in splitByNewln[i]:
            # print(splitByNewln[i:])
            # store where in the list the first Major Prep statement is seen
            begin = i
            break
    
    Requiredclasses = []
    # first we want to clear any extra stuff that isn't a class or somthing needed to group requirements
    # this is only for requirements
    for i in range(begin, len(splitByNewln)):
        if "ONE ADDITIONAL APPROVED TRANSFERABLE COURSE FOR THE MAJOR" in splitByNewln[i]:
            break
        if isvalidstr(splitByNewln[i]) and isCourse(splitByNewln[i]):
            Requiredclasses.append(splitByNewln[i].replace('\u200b', ' '))

    print(Requiredclasses)
    return Requiredclasses
'''
Things to notice: each <- marks a new articulation. if a CC course follows a <- element then it must refer to the same element
'''
def CreateDictfromtxtIrvine(file, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    RequiredClasses = getClassTextIrvine(file)
    for i in range(len(RequiredClasses)):
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')
        if '←' in RequiredClasses[i]:
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue
        cscourse = False
        
        for j in reqdict["cs"]:
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            if RequiredClasses[i] in j:
                cscourse = True
                if j not in reqqueue:

                    reqqueue.append(j)
                continue
        if cscourse == False:
            for j in reqdict["math"]:
                if RequiredClasses[i] in j and j not in reqqueue:
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
    

def CreateDictfromtxtUCSD(file, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    RequiredClasses = getClassTextIrvine(file)
    for i in range(len(RequiredClasses)):
        RequiredClasses[i] = RequiredClasses[i].replace('  ', ' ')
        if '←' in RequiredClasses[i]:
            artqueue.append([[RequiredClasses[i].replace('← ', '')]])
            continue
        cscourse = False
        
        for j in reqdict["cs"]:
            # if it is in the jth cs requirement add all these requirements into the reqqueue
            # print(RequiredClasses[i])
            # print(j)
            if RequiredClasses[i] in j:
                cscourse = True
                if j not in reqqueue:

                    reqqueue.append(j)
                continue
        if cscourse == False:
            for j in reqdict["math"]:
                if RequiredClasses[i] in j and j not in reqqueue:
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
    

