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


cwd = os.getcwd()
historical_data = "historical_data"
output_dir = os.path.join(cwd, "data", historical_data)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# start_date = "2021-05-16"
# end_date = datetime.now().strftime("%Y-%m-%d")
# start_date_2 = datetime.strptime(start_date, "%Y-%m-%d")

# num_of_days = datetime.now() - start_date_2

stock_ids = [
'159',
'160',
'163',
'164',
'166',
'171',
'172',
'174',
'176',
'177',
'178',
'179',
'180',
'181',
'182',
'183',
'184',
'185',
'186',
'187',
'188',
'189',
'190',
'192',
'194',
'195',
'198',
'200',
'201',
'203',
'204',
'205',
'207',
'209',
'210']

stock_symbols = [
'NWC',
'NIDC',
'NUBL',
'CBBL',
'DDBL',
'SANIMA',
'NABBC',
'SBBLJ',
'NICL',
'RBCL',
'NLICL',
'HGI',
'UIC',
'EIC',
'PIC',
'NIL',
'PRIN',
'SIC',
'IGI',
'NLIC',
'LICN',
'PICL',
'LGIL',
'SICL',
'NFS',
'BNL',
'NLO',
'NSM',
'NVG',
'RJM',
'GUFL',
'BSM',
'GRU',
'JSM',
'CIT',]

for i in range(len(stock_ids)):
    output_file = os.path.join(output_dir, stock_symbols[i] + ".csv")

    # openfile for writing
    _file_handle = open_file(output_file, "w")
    filewriter = csv.writer(_file_handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # header = ['sn', 'date', 'total_txns', 'total_traded_shares', 'total_traded_amt', 'max_price',
    #          'min_price', 'closing_price']
    # filewriter.writerow(header)

    base_url = "http://www.nepalstock.com/main/stockwiseprices/index/1/Date/desc/YTo0OntzOjk6InN0YXJ0RGF0ZSI7czoxMDoiMjAxNy0wMS0wMSI7czo3OiJlbmREYXRlIjtzOjEwOiIyMDIxLTA4LTExIjtzOjEyOiJzdG9jay1zeW1ib2wiO3M6MzoiMTMxIjtzOjY6Il9saW1pdCI7czo0OiIxMDAwIjt9?startDate=2009-01-01&endDate=2021-08-12&stock-symbol=" + stock_ids[i] + "&_limit=5000"

    pageurl = base_url
    print(" Parsing page: {}".format(pageurl))
    page_data = read_webpage(pageurl)

    soup = BeautifulSoup(page_data.content, 'html.parser')

    # list(soup.children)
    tds = soup.find_all('td')
    num_of_lines = len(tds) - 1
    skip = 8

    for i in range(1, num_of_lines, skip ):
        # print(soup.find_all('td')[i].get_text())

        sn = soup.find_all('td')[i].get_text()
        _date = soup.find_all('td')[i + 1].get_text()
        total_txns = soup.find_all('td')[i + 2].get_text()
        total_traded_shares = soup.find_all('td')[i + 3].get_text()
        total_traded_amt = soup.find_all('td')[i + 4].get_text()
        max_price = soup.find_all('td')[i + 5].get_text()
        min_price = soup.find_all('td')[i + 6].get_text()
        closing_price = soup.find_all('td')[i + 7].get_text()

        filewriter.writerow([sn, _date, total_txns, total_traded_shares, total_traded_amt, max_price, min_price, closing_price])
        # print(sn, _date, total_txns, total_traded_shares, total_traded_amt, max_price, min_price, closing_price)
        # print(sn + " | " + company_name + " | " +  num_of_txn + " | " +  max_price + " | " +  min_price + " | " 
        #      +  closing_price + " | " +  traded_shares + " | " +  amount + " | " +  prev_closing + " | " +  diff)
        # todays_price.append(soup.find_all('td')[i].get_text())
        # if i % 10 == 0:
            #     todays_price.append("----------------------")

    close_file(_file_handle)