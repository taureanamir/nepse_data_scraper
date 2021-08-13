from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as soup
import random
import time

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

# A randomizer for the delay
seconds = 0.1
# create a new Chrome session
driver = webdriver.Chrome('/Users/amirrajak/Downloads/chromedriver') 
# driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(30)
# driver.maximize_window()

# navigate to the application home page
driver.get("http://www.shopclues.com/mobiles-smartphones.html")
time.sleep(seconds)
time.sleep(seconds)
# Add more to range for more phones
for i in range(1):
    element = driver.find_element_by_id("moreProduct")
    driver.execute_script("arguments[0].click();", element)
    time.sleep(seconds)
    time.sleep(seconds)
html = driver.page_source
page_soup = soup(html, "html.parser")
containers = page_soup.findAll("div", {"class": "column col3"})
for container in containers:
# Add error handling
    try:
        name = container.h3.text
        price = container.find("span", {'class': 'p_price'}).text
        print("Name : " + name.replace(",", " "))
        print("Price : " + price)
    except AttributeError:
        continue
driver.quit()