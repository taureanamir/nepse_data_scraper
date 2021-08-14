from typing import Container
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from requests.api import put
import csv
import os
from datetime import date, datetime, timedelta
import time


def read_webpage(pURL):
    page = requests.get(pURL)
    return page


def open_file(filename, open_mode):
    file_handle = open(filename, open_mode)
    return file_handle


def close_file(file_handle):
    file_handle.close()


cwd = os.getcwd()
dir = "historical_data/indices"
output_dir = os.path.join(cwd, "data", dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)



sec = 5

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome('/Users/amirrajak/Downloads/chromedriver', desired_capabilities=caps)
# driver = webdriver.Chrome('/Users/amirrajak/Downloads/chromedriver') 
driver.implicitly_wait(30)
driver.maximize_window()

driver.get("https://merolagani.com/Indices.aspx")
time.sleep(sec)

# indices = ['NEPSE', 'Sensitive', 'Float', 'Sen. Float', 'Banking', 'Trading', 'Hotels And Tourism', 'Development Bank', 'Hydropower', 'Finance', 'Microfinance', 'Non-Life Insurance', 'Life Insurance', 'Manu.and Pro.', 'Others', 'Mutual Fund', 'Investment']

indices = ['Float', 'Sen. Float', 'Banking', 'Trading', 'Hotels And Tourism', 'Development Bank', 'Hydropower', 'Finance', 'Microfinance', 'Non-Life Insurance', 'Life Insurance', 'Manu.and Pro.', 'Others', 'Mutual Fund', 'Investment']

for idx in indices:
    dropdown = driver.find_element_by_xpath("//select[@title='Indices']/option[text()='" + idx + "']").click()
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_lbtnSearchIndices").click()
    time.sleep(sec)

    # openfile for writing
    output_file = os.path.join(output_dir, idx + ".csv")
    _file_handle = open_file(output_file, "w")
    filewriter = csv.writer(_file_handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ['sn' , '_date' ,  'index_value' ,  'absolute_change' ,  'percentage_change']
    filewriter.writerow(header)

    total_pages_element = driver.find_element_by_id("ctl00_ContentPlaceHolder1_PagerControl1_litRecords")
    total_pages_string = total_pages_element.text

    print(total_pages_string)
    pages = int(total_pages_string[-3:-1])

    for page in range(1, pages + 1):
        page_num = "Page " + str(page)
        title = "//a[@title='" + page_num + "']"
        try:
            element = driver.find_element_by_xpath(title)
            element.click()
            time.sleep(sec)
        except Exception as e:
            # print ("Stock: {}".format(stock))
            print(e)
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # print(page_soup)

        containers = soup.findAll("td")
        num_of_lines = len(containers)
        skip = 5
        # print("--------------------------------------------------------")
        # print(containers)
        print("--------------------------------------------------------")
        print(num_of_lines)
        print("--------------------------------------------------------")

        for i in range(0, num_of_lines, skip):
            # print(str(i) + " : " + soup.findAll("td")[i].get_text())
            sn = soup.find_all('td')[i].get_text()

            if sn == "No data available in table":
                continue
            _date = soup.find_all('td')[i + 1].get_text()
            index_value = soup.find_all('td')[i + 2].get_text()
            absolute_change = soup.find_all('td')[i + 3].get_text()
            percentage_change = soup.find_all('td')[i + 4].get_text()

            filewriter.writerow([sn , _date ,  index_value ,  absolute_change ,  percentage_change])
            print(sn , _date ,  index_value ,  absolute_change ,  percentage_change ) 
        #     #  bonus_listing_date ,  fiscal_yr)
        #     print(sn + " | " + bonus_div + " | " +  cash_div + " | " +  total_div + " | " +  book_closure_date + " | " 
        #             +  distribution_date + " | " +  bonus_listing_date + " | " +  fiscal_yr)

    close_file(_file_handle)

driver.quit()