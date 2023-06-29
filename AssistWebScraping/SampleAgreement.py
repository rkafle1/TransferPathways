from PDFGrabber import PDFGrabber
from AssistAPIInformationGetter import *
from pdfextractor import PDFExtractor
from ProcessFile import *
from writeToCSV import *
from ProcessFile import *
from pdfminer.high_level import extract_text
from Requirements import *


# grabber = PDFGrabber(getSchoolID("San Diego State University"), "Computer Science", 
#                  'CS', 0.2)
# id_to_key = grabber.get_pdfs()

# CreateDictfromtxtSDSU("San Diego State University", "Palomar College", SDSUReq)

# print(extract_text("agreements/palomarToSDSU.pdf"))

# text = extract_text("agreements/palomarToSDSU.pdf")
# splitByNewln = text.split('\n')
# print(splitByNewln)

# get rid of anything extra in the list
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
    print(Courses)
    return Courses

def DictFromTxtSDSU(UniversityName, CCName, reqdict):
    Articulations = {}
    # queues that will be used to group requirements with articulations
    reqqueue = []
    artqueue = []
    file = "agreements/report_" + str(getSchoolID(UniversityName)) +"_" + str(getSchoolID(CCName))+"_CS.pdf"
    text = extract_text("agreements/palomarToSDSU.pdf")
    RequiredClasses = text.split('\n')
    RequiredClasses = getCourses(reqdict, RequiredClasses)
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
    

generateCSVfromAgreement(DictFromTxtSDSU("San Diego State University", "Palomar College", SDSUReq), "San Diego State University", "Palomar College")