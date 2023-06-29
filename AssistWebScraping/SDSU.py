from ScrapePDFAPI import *
import Requirements
import PDFGrabber


# Run these 2 lines first to get the pdfs downloaded if it wasn't already. Comment out after
# grabber = PDFGrabber.PDFGrabber(getSchoolID("San Diego State University"), "Computer Science", 
#                  'CS', 0.2)
# id_to_key = grabber.get_pdfs()


CSVForAllAggreements("San Diego State University")
MergeCSVs("San Diego State University")
