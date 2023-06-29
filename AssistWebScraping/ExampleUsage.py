from PDFGrabber import PDFGrabber
from AssistAPIInformationGetter import *
from pdfextractor import PDFExtractor
from ProcessFile import *
from writeToCSV import *
from ProcessFile import *
from pdfminer.high_level import extract_text
# from Requirements import *
import Requirements


# this chunk downloads all CC agreements from UCI for CS.
grabber = PDFGrabber(getSchoolID("University of California, Irvine"), Requirements.CollegeCSMajor.get("University of California, Irvine"), 
                 'CS', 0.2)
id_to_key = grabber.get_pdfs()

# articulations will be the dictionary with the articulation mappings which is written to a csv in csvs/agreements directory
articulations = CreateDictfromtxtIrvine("University of California, Irvine","Palomar College", Requirements.UCIReq)
generateCSVfromAgreement(articulations, "University of California, Irvine","Palomar College")
