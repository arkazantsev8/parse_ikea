from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.firefox import 
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from tqdm import tqdm
import pandas as pd
from lxml import html
import requests
import re
from tqdm import tqdm
import pandas as pd

ITEMS = pd.read_csv('items.csv')['link'].values


options = webdriver.FirefoxOptions() 
options.add_argument("start-maximized")
fp = webdriver.FirefoxProfile('/Users/artemkazantsev/Library/Application Support/Firefox/Profiles/xq2rpstm.default')
driver = webdriver.Firefox(fp)
driver.get('https://www.ikea.com/pl/pl')
#accept cookies
driver.find_element(By.ID, "onetrust-accept-btn-handler").click() 

for i in tqdm(ITEMS):
    driver.get(i)
    time.sleep(1)
    #for the case when item is unavailable
    try:
        driver.find_element(By.XPATH, "//button[@class='pip-btn pip-btn--emphasised']").click()
    except: 
        pass
#time to finish order
time.sleep(600)
