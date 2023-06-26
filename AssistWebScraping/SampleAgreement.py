from PDFGrabber import PDFGrabber
from AssistAPIInformationGetter import *
from pdfextractor import PDFExtractor
from ProcessFile import *
from writeToCSV import *
from ProcessFile import *
from pdfminer.high_level import extract_text
# from Requirements import *


text = extract_text("agreements/SampleAgreements.pdf")

print(text)

print(extract_text("agreements/report_120_3_CS.pdf"))