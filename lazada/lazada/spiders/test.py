import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
from fake_useragent import UserAgent
import time
from selenium.webdriver.common.action_chains import ActionChains

class TestSpider(scrapy.Spider):
    name = 'test'
    #allowed_domains = ['www.lazada.com.my']
    start_urls = ['https://www.lazada.com.my/products/special-promotion-mcafee-total-protection-1-device-1-year-i1126152789-s3184504736.html?spm=a2o4k.searchlistcategory.list.3.71344531hl8JIk&search=1&freeshipping=1']

    def parse(self, response):
        path = which("chromedriver")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        ua = UserAgent()
        userAgent = ua.random
        #print(userAgent)
        chrome_options.add_argument(f'user-agent={userAgent}')
        driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
        driver.set_window_size(1920,1080)
        driver.get(response.url)
        time.sleep(3)