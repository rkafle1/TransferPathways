
from Requirements import *
import sys
#absolute path for the assist web scraping folder
sys.path.insert(1, 'C:/Users/a2576/Documents/GitHub/TransferPathways/AssistWebScraping')
import ProcessFile
from AssistAPIInformationGetter import *
from writeToCSV import *
import statistics
import pandas as pd
import numpy as np
keyterms = ['']
CCids = getCCIdList()