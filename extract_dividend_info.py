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
historical_dividend = "historical_data/dividend"
output_dir = os.path.join(cwd, "data", historical_dividend)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# start_date = "2021-05-16"
# end_date = datetime.now().strftime("%Y-%m-%d")
# start_date_2 = datetime.strptime(start_date, "%Y-%m-%d")

# num_of_days = datetime.now() - start_date_2
# YHL = No dividend info in the site
# 'NIB', 'NABIL', 'SCB', 'HBL', 'SBI', 'NBB', 'EBL', 'BOKL', 'NICA', 'MBL', 'LBL', 'KBL', 'NCCB', 'SBL',
stocks = ['CBBL', 'DDBL', 'SANIMA', 'NABBC', 'SBBLJ', 'NICL', 'RBCL', 'NLICL', 'HGI', 'UIC', 'EIC', 'PIC', 'NIL', 'PRIN', 'SIC', 'IGI', 'NLIC', 'LICN', 'PICL', 'LGIL', 'SICL', 'NFS', 'BNL', 'NLO', 'NSM', 'NVG', 'RJM', 'GUFL', 'BSM', 'GRU', 'JSM', 'CIT', 'AVU', 'BNT', 'HBT', 'BSL', 'UNL', 'SFC', 'NKU', 'SBPP', 'BFC', 'FHL', 'SRS', 'LFC', 'GFCL', 'NBBU', 'HDL', 'PFL', 'NMB', 'UFL', 'SIFC', 'CFCL', 'SYFL', 'JFL', 'PRVU', 'SFCL', 'CMB', 'SFFIL', 'GMFIL', 'SWBBL', 'ICFC', 'EDBL', 'EBLCP', 'SIL', 'CEFL', 'NTC', 'PROFL', 'GBIME', 'CZBIL', 'PCBL', 'LBBL', 'SRBL', 'AHPC', 'CFL', 'MDB', 'ALICL', 'PLIC', 'NLBBL', 'ADBL', 'ODBL', 'MLBL', 'SLICL', 'GBBL', 'JBBL', 'KNBL', 'GDBL', 'HATH', 'KRBL', 'HFL', 'GLICL', 'CORBL']
sec = 5

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome('/Users/amirrajak/Downloads/chromedriver', desired_capabilities=caps)
# driver = webdriver.Chrome('/Users/amirrajak/Downloads/chromedriver') 
driver.implicitly_wait(30)
driver.maximize_window()

for stock in stocks:
    driver.get("https://www.sharesansar.com/company/" + stock)
    time.sleep(sec)
    try:
        element = driver.find_element_by_id("btn_cdividend")
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        print ("Stock: {}".format(stock))
        print(e)
    time.sleep(sec)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # print(page_soup)

    containers = soup.findAll("td")
    num_of_lines = len(containers)
    skip = 8
    # print("--------------------------------------------------------")
    # print(containers)
    print("--------------------------------------------------------")
    print(stock)
    print(num_of_lines)
    print("--------------------------------------------------------")

    for j in range(1, num_of_lines):
        if soup.find_all('td')[j].get_text() == "Website Link":
            start_at = j+2
            print("start_at: {}".format(start_at))
            break

    # openfile for writing
    output_file = os.path.join(output_dir, stock + ".csv")
    _file_handle = open_file(output_file, "w")
    filewriter = csv.writer(_file_handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ['sn', 'bonus_dividend', 'cash_dividend', 'total_dividend', 'book_closure_date', 'distribution_date',
             'bonus_listing_date', 'fiscal_yr']
    filewriter.writerow(header)

    for i in range(start_at, num_of_lines, skip):
        print(str(i) + " : " + soup.findAll("td")[i].get_text())
        sn = soup.find_all('td')[i].get_text()

        if sn == "No data available in table":
            continue
        bonus_div = soup.find_all('td')[i + 1].get_text()
        cash_div = soup.find_all('td')[i + 2].get_text()
        total_div = soup.find_all('td')[i + 3].get_text()
        book_closure_date = soup.find_all('td')[i + 4].get_text()
        distribution_date = soup.find_all('td')[i + 5].get_text()
        bonus_listing_date = soup.find_all('td')[i + 6].get_text()
        fiscal_yr = soup.find_all('td')[i + 7].get_text()

        filewriter.writerow([sn , bonus_div ,  cash_div ,  total_div ,  book_closure_date ,  
                              distribution_date ,  bonus_listing_date ,  fiscal_yr])
        # print(sn , bonus_div ,  cash_div ,  total_div ,  book_closure_date ,  distribution_date , 
        #  bonus_listing_date ,  fiscal_yr)
        print(sn + " | " + bonus_div + " | " +  cash_div + " | " +  total_div + " | " +  book_closure_date + " | " 
                +  distribution_date + " | " +  bonus_listing_date + " | " +  fiscal_yr)

    close_file(_file_handle)

driver.quit()