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
import re

with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Phone No","Site Address","Site City","Site State","Site zip","Location hours","Storage Hours","Features","Benfits","Unit name","Description","Price"])

ul = "https://www.uhaul.com/Storage/"
path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(3)
link = ""

def scrape(link):
    try:
        btn = driver.find_elements_by_xpath("//form[@class='collapse ']/button")
        for i in range(0,len(btn)):
            driver.find_elements_by_xpath("//form[@class='collapse ']/button")[i].click()
            time.sleep(2)
            try:   
                driver.find_element_by_xpath("//a[@id='viewAllFeatures']").click()
                time.sleep(2)
            except:
                print("Scroll bar doesn't exist for features.")
            html = driver.page_source
            resp = Selector(text=html)

            name = resp.xpath("normalize-space(//h2[@class='collapse-half text-dull text-xl text-semibold']/text())").extract_first()
            phone_no = resp.xpath("normalize-space(//div[@class='medium-divider']/p/a/text())").extract_first()
            site_address = resp.xpath("normalize-space((//address[@class='collapse-half']/text())[1])").extract_first()
            site_city_state_zip = resp.xpath("normalize-space((//address[@class='collapse-half']/text())[2])").extract_first()
            try:
                site_city_state_zip = str(site_city_state_zip)
                site_city = re.findall(r"^[^,]+",site_city_state_zip)
                site_state = re.findall(r"\s\w\w\s",site_city_state_zip)
                site_zip = re.findall(r"\d.*",site_city_state_zip)
            except:
                site_city = None
                site_state = None
                site_zip = None

            location_hours = resp.xpath("(//ul[@class='no-bullet condensed'])[1]/li/text()").getall()
            storage_hours = resp.xpath("((//ul[@class='no-bullet condensed'])[1]/following-sibling::ul)[1]/li/text()").getall()
            features = resp.xpath("//div[@id='completeFeatureList']//li/text()").getall()
            benfits = resp.xpath("//div[@class='callout flat']/ul[@class='tag-list']/li//text()").getall()

            name_lis,description,price=[],[],[]
            lis = resp.xpath("//ul[@class='no-bullet uhjs-units-small uhjs-unit-list']/li")
            for li in lis:
                nam = li.xpath("normalize-space(.//h4[@class='collapse']/text())").get()
                name_lis.append(nam)

                des = li.xpath("normalize-space(.//p[@class='collapse-half']/text())").get()
                description.append(des)

                pri = li.xpath(".//b[@class='text-lg']/text()").get()
                price.append(pri)

            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name,phone_no,site_address,site_city,site_state,site_zip,location_hours,storage_hours,features,benfits,name_lis,description,price])
                print("Data Saved in CSV:")
            driver.get(link)
            time.sleep(2)
    except:
        print("There is nothing there to scrap.")
def next_page():
    link = driver.current_url
    scrape(link)
    try:
        nex = driver.find_element_by_xpath("(//li[@class='cell small-6 medium-shrink']/a[contains(@href,'Next')])[2]")
        if nex:
            nex.click()
            time.sleep(2)
            next_page()
    except:
        print("Search Contains only one page")


print("Enter the complete addres where you want to extract the data:")
search_input = input()


search = driver.find_element_by_xpath("//input[@id='movingFromInput']")
time.sleep(2)
search.clear()
search.send_keys(search_input)
search.send_keys(Keys.ENTER)
time.sleep(3)
next_page()

