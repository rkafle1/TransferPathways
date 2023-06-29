from PDFGrabber import PDFGrabber
from AssistAPIInformationGetter import *
from pdfextractor import PDFExtractor
from ProcessFile import *
from writeToCSV import *
from ProcessFile import *
from pdfminer.high_level import extract_text
from Requirements import *


# grabber = PDFGrabber(getSchoolID("University of California, Irvine"), CollegeCSMajor.get("University of California, Irvine"), 
#                  'CS', 0.2)
# id_to_key = grabber.get_pdfs()

CCList = getCCIdList()

# for cc in CCList:
#     articulations = CreateDictfromtxtIrvine("University of California, Irvine",getSchoolFromID(cc), UCIReq)
#     generateCSVfromAgreement(articulations, "University of California, Irvine",getSchoolFromID(cc))

MergeUniversityCSVs("University of California, Irvine", CCList)