from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
from fake_useragent import UserAgent
import time
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
import csv
from selenium.webdriver.support.ui import Select
import re
count = 0
with open('dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["title","sku","DESCRIPTION","price_for_25","price_for_100","price_for_250","price_for_500","price_for_1000","net_price","net_price_bundle"])

def scrap(count):
    html = (driver.page_source).encode('utf-8')
    resp = Selector(text=html)
    rows = resp.xpath("//table[@id='super-product-table']/tbody/tr")
    for row in rows:
        title = row.xpath("normalize-space(.//a[@class='action action-link product-name']/text())").extract_first()
        sku = row.xpath("normalize-space(.//span[@class='product-item-sku']/text())").extract_first()
        DESCRIPTION = row.xpath("normalize-space(.//td[@class='product description product-item-description offset-on-mobile']/text())").extract_first()
        price_for_25 = row.xpath("normalize-space(.//dl[@class='cat-tier-price']/dt[1]/text())").extract_first()
        price_for_100 = row.xpath("normalize-space(.//dl[@class='cat-tier-price']/dt[2]/text())").extract_first()
        price_for_250 = row.xpath("normalize-space(.//dl[@class='cat-tier-price']/dt[3]/text())").extract_first()
        price_for_500 = row.xpath("normalize-space(.//dl[@class='cat-tier-price']/dt[4]/text())").extract_first()
        price_for_1000 = row.xpath("normalize-space(.//dl[@class='cat-tier-price']/dt[5]/text())").extract_first()
        net_price = row.xpath("normalize-space(.//div[@class='bundle-pricing']/strong/text())").extract_first()
        net_price_bundle = row.xpath("normalize-space(.//div[@class='bundle-pricing']/span/text())").extract_first()

        print()
        print("Title",title)
        print("SKU",sku)
        print("DESCRIPTION",DESCRIPTION)
        print("price_for_25",price_for_25)
        print("price_for_100",price_for_100)
        print("price_for_250",price_for_250)
        print("price_for_500",price_for_500)
        print("price_for_1000",price_for_1000)
        print("net_price",net_price)
        print("net_price_bundle",net_price_bundle)

        with open('dataset.csv', 'a', newline='',encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([title,sku,DESCRIPTION,price_for_25,price_for_100,price_for_250,price_for_500,price_for_1000,net_price,net_price_bundle])
            count = count + 1
            print("Data Saved in CSV: ",count)     

    return count



ul = "https://www.packagingprice.com/corrugated-boxes.html"

path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(30)
try:
    driver.find_element_by_xpath("//button[@class='CloseButton__ButtonElement-sc-79mh24-0 cRdofU karlstad-CloseButton karlstad-close karlstad-ClosePosition--top-right']").click()
    time.sleep(5)
except:
    print("Pop up didn't appear")

pages = driver.find_elements_by_xpath("//h2[@class='h3 top-category-title']/parent::a")
for pg in range(0,len(pages)):
    driver.find_elements_by_xpath("//h2[@class='h3 top-category-title']/parent::a")[pg].click()
    time.sleep(10)
    items = driver.find_elements_by_xpath("//div[@class='product-item-info']/a[@class='product photo product-item-photo']")
    for i in range(0,len(items)):
        driver.find_elements_by_xpath("//div[@class='product-item-info']/a[@class='product photo product-item-photo']")[i].click()
        time.sleep(10)
        while True:
            try:
                btn = driver.find_element_by_xpath("//a[@class='action  next']")
                if btn:
                    count = scrap(count)
                    btn = driver.find_element_by_xpath("//a[@class='action  next']")
                    btn.click()
                    time.sleep(15)
                else:
                    break
            except:
                count = scrap(count)
                break






#         except:
#             print("Search results")    
#         driver.get("https://www.arcountydata.com/propsearch.asp")
#         time.sleep(4) 