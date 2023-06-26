from bs4 import BeautifulSoup
import requests
import pandas as pd

#url object
url = "https://assist.org/transfer/results?year=74&institution=56&view=transferability&type=CSUTC&viewBy=dept&viewByKey=computer%20science%20and%20information%20systems%20-%20computer%20science"
# create object page
page = requests.get(url)
print(page)
soup = BeautifulSoup(page.text, 'lxml')



''' 
this file contains the function to scrape the CSU transferable courses for all community colleges for the 2023 - 2024 year
'''

def getWebPage(CCName):
    url = "https://assist.org/transfer/results/preview?year=73&institution=56&type=CSUTC&view=transferability&viewBy=dept&viewByKey=computer%20science%20and%20information%20systems%20-%20computer%20science"
    content = requests.get(url).text
    with open('CSUTransferrableCourses.html', 'w') as f:
        soup = BeautifulSoup(content, 'lxml')
        f.write(soup.prettify())

    
getWebPage("somthing")