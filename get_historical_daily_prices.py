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
daily_prices_dir = "daily_prices"
output_dir = os.path.join(cwd, "output", daily_prices_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


start_date = "2021-05-16"
end_date = datetime.now().strftime("%Y-%m-%d")
start_date_2 = datetime.strptime(start_date, "%Y-%m-%d")

num_of_days = datetime.now() - start_date_2

for i in range(num_of_days.days):
    today = start_date_2 + timedelta(i)
    today = today.strftime("%Y-%m-%d")
    output_file = os.path.join(output_dir, today + ".csv")

    # openfile for writing
    _file_handle = open_file(output_file, "w")
    filewriter = csv.writer(_file_handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ['sn', 'company_name', 'num_of_txn', 'max_price', 'min_price', 'closing_price',
                'traded_shares', 'amount', 'prev_closing', 'diff']
    filewriter.writerow(header)

    base_url = "http://www.nepalstock.com/main/todays_price/index/1/YTozOntzOjk6InN0YXJ0RGF0ZSI7czoxMDoiMjAyMS0wOC0wMSI7czoxMjoic3RvY2stc3ltYm9sIjtzOjA6IiI7czo2OiJfbGltaXQiO3M6MjoiMjAiO30?startDate=" + today + "&stock-symbol=&_limit=300"
    todays_price = []

    pageurl = base_url
    print(" Parsing page: {}".format(pageurl))
    page_data = read_webpage(pageurl)

    soup = BeautifulSoup(page_data.content, 'html.parser')

    # list(soup.children)
    tds = soup.find_all('td')
    num_of_lines = len(tds) - 7 # last 7 lines are not reqd.

    for i in range(1, num_of_lines, 10 ):
        # print(soup.find_all('td')[i].get_text())
        if i == 1:
            continue
        sn = soup.find_all('td')[i].get_text()
        company_name = soup.find_all('td')[i + 1].get_text()
        num_of_txn = soup.find_all('td')[i + 2].get_text()
        max_price = soup.find_all('td')[i + 3].get_text()
        min_price = soup.find_all('td')[i + 4].get_text()
        closing_price = soup.find_all('td')[i + 5].get_text()
        traded_shares = soup.find_all('td')[i + 6].get_text()
        amount = soup.find_all('td')[i + 7].get_text()
        prev_closing = soup.find_all('td')[i + 8].get_text()
        diff = soup.find_all('td')[i + 9].get_text()
        diff = diff.split()[0]

        filewriter.writerow([sn, company_name, num_of_txn, max_price, min_price, closing_price, traded_shares, amount, prev_closing, diff])
        # print(sn, company_name, num_of_txn, max_price, min_price, closing_price, traded_shares, amount, prev_closing, diff)
        # print(sn + " | " + company_name + " | " +  num_of_txn + " | " +  max_price + " | " +  min_price + " | " 
        #      +  closing_price + " | " +  traded_shares + " | " +  amount + " | " +  prev_closing + " | " +  diff)
        # todays_price.append(soup.find_all('td')[i].get_text())
        # if i % 10 == 0:
            #     todays_price.append("----------------------")

    close_file(_file_handle)