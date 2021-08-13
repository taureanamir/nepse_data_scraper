from bs4.element import PYTHON_SPECIFIC_ENCODINGS
import requests
from bs4 import BeautifulSoup
from requests.api import put
import csv
import os
from datetime import date, datetime, timedelta


def read_webpage(pURL):
    page = requests.get(pURL)
    return page


def open_file(filename, open_mode):
    file_handle = open(filename, open_mode)
    return file_handle


def close_file(file_handle):
    file_handle.close()


def clean_data(pData):
    pData = pData.replace('\n', '')
    pData = pData.strip()
    return pData


cwd = os.getcwd()
output_dir = os.path.join(cwd, "output")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file = os.path.join(output_dir, "stocks_list" + ".csv")


base_url = "http://www.nepalstock.com/company/index/1/stock-name/desc/YTo0OntzOjEwOiJzdG9jay1uYW1lIjtzOjA6IiI7czoxMjoic3RvY2stc3ltYm9sIjtzOjA6IiI7czo5OiJzZWN0b3ItaWQiO3M6MDoiIjtzOjY6Il9saW1pdCI7czozOiIzMDAiO30?stock-name=&stock-symbol=&sector-id=&_limit=300"

pageurl = base_url
print(" Parsing page: {}".format(pageurl))
page_data = read_webpage(pageurl)

soup = BeautifulSoup(page_data.content, 'html.parser')

# list(soup.children)
tds = soup.find_all('td')
num_of_lines = len(tds)

stock_detail = []

for i in range(7, 1777, 6):
    # print(soup.find_all('td')[i].get_text())

    sn = soup.find_all('td')[i].get_text()
    # company_name = soup.find_all('td')[i + 1].get_text()
    stock_name = soup.find_all('td')[i + 2].get_text()
    stock_symbol = soup.find_all('td')[i + 3].get_text()
    sector = soup.find_all('td')[i + 4].get_text()

    stock_name = clean_data(stock_name)
    stock_symbol = clean_data(stock_symbol)
    sector = clean_data(sector)

    stock_detail.append([sn, stock_name, stock_symbol, sector])

    # filewriter.writerow([sn, company_name, num_of_txn, max_price, min_price, closing_price])
    # print(sn+ " | " +  stock_name+ " | " + stock_symbol+ " | " + sector )



stock_ids = []

for i in range(6, num_of_lines - 1):
    anchor_tag = tds[i].find('a')
    if anchor_tag is not None:
        # print (anchor_tag.text) 
        href = anchor_tag['href']
        href = clean_data(href)
        stock_id = href.split("/")[-1]
        stock_ids.append(stock_id)

# openfile for writing
_file_handle = open_file(output_file, "w")
filewriter = csv.writer(_file_handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
header = ['sn', 'id', 'stock_name', 'symbol', 'sector']
filewriter.writerow(header)

for i in range(len(stock_ids)):
    print(stock_ids[i], stock_detail[i])
    sn = stock_detail[i][0]
    s_id = stock_ids[i]
    stock_name = stock_detail[i][1]
    symbol = stock_detail[i][2]
    sector = stock_detail[i][3]

    filewriter.writerow([sn, s_id, stock_name, symbol, sector])

close_file(_file_handle)