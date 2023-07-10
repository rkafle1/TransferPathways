from PDFGrabber import PDFGrabber
from AssistAPIInformationGetter import *
import operator
from ProcessFile import *
from writeToCSV import *
from ProcessFile import *
from pdfminer.high_level import extract_text
from Requirements import *


# grabber = PDFGrabber(getSchoolID("University of California, Merced"), "Computer Science and Engineering, B.S. ", 
#                  'CS', .7)
# id_to_key = grabber.get_pdfs()



# text = extract_text("agreements/report_144_56_CS.pdf")
# splitByNewln = text.split('\n')
# print(splitByNewln)


# get rid of anything extra in the list
def getCoursesUCB(reqdict, splitlist):

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

print(generateCSVfromAgreement(DictFromTxtUCB("University of California, Merced", "Palomar College", UCMReq), "University of California, Merced", "Palomar College"))
