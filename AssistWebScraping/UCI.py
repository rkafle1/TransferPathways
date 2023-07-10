from PDFGrabber import PDFGrabber
from AssistAPIInformationGetter import *
from ScrapePDFAPI import *
from ProcessFile import *
from writeToCSV import *
from ProcessFile import *
from pdfminer.high_level import extract_text
from Requirements import *


# grabber = PDFGrabber(getSchoolID("University of California, Irvine"), CollegeCSMajor.get("University of California, Irvine"), 
#                  'CS', 0.2)
# id_to_key = grabber.get_pdfs()

CSVForAllAggreements("University of California, Irvine")
MergeCSVs("University of California, Irvine")

