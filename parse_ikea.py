from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
driver.get('https://www.ikea.com/pl/pl')
time.sleep(60) #time to accept cookies and enter postal index for delivery and closest store

# Request the page
def extract_item_details(item_url):
    page = requests.get(item_url)
    tree = html.fromstring(page.content) 
    item = {} 
    item['link'] = item_url
    item['name'] = tree.xpath("//span[@class='pip-header-section__title--big notranslate']/text()")[0]
    item['group'] = [str(x) for x in tree.xpath("//a[@class='bc-breadcrumb__link bc-link bc-link--black']/span/text()")][1]
    item['description'] = tree.xpath("//span[@class='pip-header-section__description-text']/text()")[0]
    price_int = tree.xpath("//span[@class='pip-temp-price__integer']/text()")[0]
    price_decimal = tree.xpath("//span[@class='pip-temp-price__decimal']/text()")
    item['price'] = float(price_int.replace(' ','')) + float(price_decimal[0])/100 if not bool(re.search(',-',price_int)) else float(price_int.replace(',-','').replace(' ',''))

    driver.get(i)
    time.sleep(3)
    try:
        dostawa = driver.find_element(By.XPATH, "//div[@class='pip-product__buy-module-item-avaialability-group']")
        item['dostawa'] = dostawa.text
    except: 
        item['dostawa'] = ''
    return item

items = []
for i in tqdm(ITEMS[:2]):
    items.append(extract_item_details(i))

ikea_data = pd.DataFrame(items)
ikea_data['dostawa'] = ikea_data['dostawa'].apply(lambda x: x.replace('\n', ' '))
ikea_data['delivery'] = ikea_data['dostawa'].apply(lambda x: bool(re.findall('Dostępne', x)))
ikea_data['janki'] = ikea_data['dostawa'].apply(lambda x: bool(re.findall('Sklep - Dostępny', x)))
ikea_data = ikea_data.merge(pd.read_csv('items.csv'), how='left', on='link')[['link', 'image', 'name', 'group', 'description', 'delivery', 'janki', 'price']]

ikea_data.to_csv('ikea_data.csv', index=False)