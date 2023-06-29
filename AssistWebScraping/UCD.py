from PDFGrabber import PDFGrabber
from AssistAPIInformationGetter import *
from pdfextractor import PDFExtractor
from ProcessFile import *
from writeToCSV import *
from ProcessFile import *
from pdfminer.high_level import extract_text
from Requirements import *


grabber = PDFGrabber(getSchoolID("University of California, San Diego"), CollegeCSMajor.get("University of California, San Diego"), 
                 'CS', 0.2)
id_to_key = grabber.get_pdfs()

# text = extract_text("agreements/report_89_2_CS.pdf")
# splitByNewln = text.split('\n')
# print(splitByNewln)