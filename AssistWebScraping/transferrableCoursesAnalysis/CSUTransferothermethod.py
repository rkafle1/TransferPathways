from selenium import webdriver
from selenium.webdriver.common.by import By

website = 'https://assist.org/transfer/results/preview?year=74&institution=56&type=CSUTC&view=transferability&viewBy=dept&viewByKey=computer%20science%20and%20information%20systems%20-%20computer%20science'

url = 'https://www.adamchoi.co.uk/overs/detailed'
path = "C:/Users/richa/Downloads/chromedriver/chromedriver"

driver = webdriver.Chrome()
driver.get(website)
element = driver.find_element(By.XPATH, '/html/body/app-root/div[2]/app-report-preview/div/awc-transferable-courses')
print("this is printing" , element.text)
driver.quit()
# table path: body, app-root, div, app-transfer, div role ="main" class = "child", app results, section id = "view-results" class = "results", 
# div class = "resultsBox"