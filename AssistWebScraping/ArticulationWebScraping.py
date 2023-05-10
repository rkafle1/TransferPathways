from PDFGrabber import PDFGrabber
from AssistAPIInformationGetter import *
from pdfextractor import PDFExtractor
# Dictionary which consists of the CS major name for the specific university
# Todo: Put this data into a CSV file and create dictionary using that instead.
CollegeCSMajor = {"University of California, San Diego": "Computer Science B.S.", "University of California, Irvine": "Computer Science, B.S.",
                   "University of California, Santa Barbara": "Computer Science, B.S.", "University of California, Riverside": "Computer Science, B.S.",
                   "University of California, Berkeley": "Computer Science, Lower Division B.A.", "University of California, Davis": "Computer Science B.S.",
                   "University of California, Los Angeles": "Computer Science/B.S.", "University of California, Santa Cruz": "Computer Science B.S.",
                   "University of California, Merced": "Computer Science and Engineering, B.S."}

# grabber = PDFGrabber(120, 'Software Engineering, B.S.', 'SWE', 0.2)

# grabber = PDFGrabber(getSchoolID("University of California, Irvine"), CollegeCSMajor.get("University of California, Irvine"), 
#                  'CS', 0.2)
# id_to_key = grabber.get_pdfs()

extractor = PDFExtractor('report_128_150_CS.pdf')

# reqs_to_equivs = extractor.process_page()


# get all pdf agreements for every combination of uc and cc
# for key in CollegeCSMajor:
#     grabber = PDFGrabber(getSchoolID(key), CollegeCSMajor.get(key), 
#                  'CS', 0.2)
#     id_to_key = grabber.get_pdfs()