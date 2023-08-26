from PDFGrabber import *
import ScrapePDFMethods
import AssistAPIInformationGetter
import Requirements

# this is an example of how to get the pdfs for a university. Once you run this you don't have to run the same call again. In this case SDSU: 
grabber = PDFGrabber(AssistAPIInformationGetter.getSchoolID("San Diego State University"), "Computer Science", 
                 'CS', 0.2)
id_to_key = grabber.get_pdfs()

# To generate the scraped agreements csvs with the course mappings:
# this gets the mappings for all SDSU's agreements
ScrapePDFMethods.CSVForAllAggreements("San Diego State University", Requirements.SDSUReq)
