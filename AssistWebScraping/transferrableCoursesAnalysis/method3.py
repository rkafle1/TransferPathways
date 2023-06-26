from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys

website = 'https://assist.org/transfer/results/preview?year=74&institution=56&type=CSUTC&view=transferability&viewBy=dept&viewByKey=computer%20science%20and%20information%20systems%20-%20computer%20science'

path = "C:/Users/richa/Downloads/chromedriver/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome()

search_query = "life"

with webdriver as driver:

    driver.get(website)
    element = driver.find_elements(By.TAG_NAME, 'tr')


