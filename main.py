import os
import time

import urllib
import urllib.request
from urllib.error import URLError, HTTPError
from urllib.parse import quote_plus

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

CHROMIUM_PATH = './chromedriver.exe'

base_url  = 'https://www.gapminder.org/dollar-street/'
#topics = ['arm-watches', 'armchairs', 'beds', 'bikes', 'bowls', 'cups']
topics = ['arm-watches']
save_dir = './img/'

# maximum number of images in one category (to prevent mem overflow)
MAX_NUM = 60

def urlopen_chrome(url): 
    try: 
        headers = {'User-Agent': 'Chrome/66.0.3359.181'}
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req)
    except HTTPError as e:
        err = e.read()
        code = e.getcode()
        print(code, err)
    return html

def js_execute(url):
    #options = webdriver.ChromeOptions()
    #options.add_argument('user-agent=Chrome/66.0.3359.181')
    #client = webdriver.Chrome(CHROMIUM_PATH, chrome_options=options)
    client = webdriver.Chrome(executable_path=CHROMIUM_PATH)
    client.get(url)
    return client

# make save directory structure
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)
for topic in topics:
    path = save_dir + topic
    if not os.path.isdir(path):
        os.mkdir(path)

for topic in topics:
    url = base_url + '?topic=' + topic + '&media=image'
    images = []
    incomes = []
    countries = []
    # crawl image sources and data
    with js_execute(url) as client:
        for i in range(1, MAX_NUM):
            try:
                img_obj = client.find_element_by_xpath('/html/body/div[2]/main/div[1]/div[1]/div['+str(i)+']/a[1]/div[1]/div[2]/div[1]/img')
                img_source = img_obj.get_attribute('src')
                
                img_income_obj = client.find_element_by_xpath('/html/body/div[2]/main/div[1]/div[1]/div['+str(i)+']/a[1]/div[1]/div[1]/span[1]')
                img_income = img_income_obj.get_attribute('innerHTML')

                img_country_obj = client.find_element_by_xpath('/html/body/div[2]/main/div[1]/div[1]/div['+str(i)+']/a[1]/div[1]/div[1]/span[2]')
                img_country = img_country_obj.get_attribute('innerHTML')
            except NoSuchElementException as e:
                break
            images.append(img_source)
            incomes.append(img_income)
            countries.append(img_country)
    print('Category crawl complete : ' + topic)
    print(incomes)
    # save label (file_name income country)
    with open(save_dir + topic + '/' + 'label.txt', 'w') as label:
        for i in range(len(images)):
            label.write(images[i] + ' ')
            label.write(incomes[i] + ' ')
            label.write(countries[i] + '\n')
    # save images
    for img_num in range(len(images)):
        img_url = images[img_num]
        with urlopen_chrome(img_url) as f:
            with open(save_dir + topic + '/' + str(img_num) + '.jpg', 'wb') as h:
                img_file = f.read()
                h.write(img_file)
    print('Category save complete : ' + topic)



