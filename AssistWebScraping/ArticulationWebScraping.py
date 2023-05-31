from PDFGrabber import PDFGrabber
from AssistAPIInformationGetter import *
from pdfextractor import PDFExtractor
from ProcessFile import *
from writeToCSV import *
import os
from ProcessFile import *
from pdfminer.high_level import extract_text
# Dictionary which consists of the CS major name for the specific university
# Todo: Put this data into a CSV file and create dictionary using that instead.
CollegeCSMajor = {"University of California, San Diego": "Computer Science B.S.", "University of California, Irvine": "Computer Science, B.S.",
                   "University of California, Santa Barbara": "Computer Science, B.S.", "University of California, Riverside": "Computer Science, B.S.",
                   "University of California, Berkeley": "Computer Science, Lower Division B.A.", "University of California, Davis": "Computer Science B.S.",
                   "University of California, Los Angeles": "Computer Science/B.S.", "University of California, Santa Cruz": "Computer Science B.S.",
                   "University of California, Merced": "Computer Science and Engineering, B.S."}

# grabber = PDFGrabber(120, 'Software Engineering, B.S.', 'SWE', 0.2)


# writeToCSV("agreements/report_120_5_CS.pdf")

# grabber = PDFGrabber(getSchoolID("University of California, Irvine"), CollegeCSMajor.get("University of California, Irvine"), 
#                  'CS', 0.2)
# id_to_key = grabber.get_pdfs()


# maker = DatabaseMaker('UCI', 'CS', id_to_key)
# maker.add_classes()
# text = extract_text('agreements/report_120_3_CS.pdf')
# print(text)
# splitByNewln = text.split
# extractor =  PDFExtractor('agreements/report_120_3_CS.pdf')
# reqs_to_equivs = extractor.dict_from_file()
# print(reqs_to_equivs)


# get all pdf agreements for every combination of uc and cc
# for key in CollegeCSMajor:
#     grabber = PDFGrabber(getSchoolID(key), CollegeCSMajor.get(key), 
#                  'CS', 0.2)
#     id_to_key = grabber.get_pdfs()





# start of better code: 
IrvineReq = {"cs": [["I&C SCI 31 - Introduction to Programming (4.00)", "I&C SCI 32 - Programming with Software Libraries (4.00)", "I&C SCI 33 - Intermediate Programming (4.00)"]],
             "math":[["MATH 2A - Single-Variable Calculus (4.00)"], ["MATH 2B - Single-Variable Calculus (4.00)"]], "1 additional": True}
articulations = CreateDictfromtxtUCI('agreements/report_120_3_CS.pdf', IrvineReq)
generateCSVfromAgreement(articulations, "csvs/agreements/report_120_3_CS.csv")