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

class ProductSpider(scrapy.Spider):
    name = 'product'
    #allowed_domains = ['www.lazada.com.my']
    start_urls = ['https://www.lazada.com.my/shop-software/?spm=a2o4k.pdp_revamp.breadcrumb.3.54b05c1aRaQ9f5']

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
        n=0
        while True:
            if n == 0:
                try:
                    btn_info_page = driver.find_elements_by_xpath("//div[@class='c16H9d']/a[@age='0']")
                    if btn_info_page:
                        for wsa in range(0,len(btn_info_page)):     
                            btn_info_page = driver.find_elements_by_xpath("//div[@class='c16H9d']/a[@age='0']")[wsa]
                            if btn_info_page:
                                abcd = btn_info_page.get_attribute("href")
                                image_url_link = driver.find_elements_by_xpath("//img[@class='c1ZEkM ']")[wsa]
                                img = image_url_link.get_attribute("src")
                                Discounted = driver.find_elements_by_xpath("//span[@class='c13VH6']")[wsa]
                                dis = Discounted.text
                                regular = driver.find_elements_by_xpath("//del[@class='c13VH6']")[wsa]
                                reg = regular.text
                                btn_info_page.click()
                                time.sleep(3)
                                try:
                                    driver.execute_script("window.scrollTo(0, 900)") 
                                    time.sleep(3)
                                    driver.execute_script("window.scrollTo(900, 1800)") 
                                    time.sleep(4)
                                    try:
                                        self.html = driver.page_source
                                        resp = Selector(text=self.html)
                        
                                        abc = resp.xpath("//a[@class='pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name']/@href").get()
                                        absolute_url = f"https:{abc}"
                                        yield{
                                            'Title':resp.xpath("//h1[@class='pdp-mod-product-badge-title']/text()").get(),
                                            'Product_Type':resp.xpath("(//a[@class='breadcrumb_item_anchor']/span/text())[3]").get(),
                                            'Catagory':resp.xpath("//a[@class='breadcrumb_item_anchor']/span/text()").getall(),
                                            'Content':resp.xpath("//meta[@name='description']/@content").get(),
                                            'Stock':resp.xpath("//span[@class='quantity-content-default']/text()").get(),
                                            'Brand':resp.xpath("//div[@class='pdp-product-brand']/a/text()").getall(),
                                            'Wrranty Period':resp.xpath("(//div[@class='html-content key-value']/text())[5]").get(),
                                            'Model':resp.xpath("(//div[@class='html-content key-value']/text())[4]").get(),
                                            'SKU':resp.xpath("(//div[@class='html-content key-value']/text())[2]").get(),
                                            'Receiving_item':resp.xpath("//div[@class='html-content box-content-html']/text()").get(),
                                            'Detail_Description':resp.xpath("//div[@class='html-content pdp-product-highlights']/ul/li/text()").getall(),
                                            'Rating out of 5':resp.xpath("//span[@class='score-average']/text()").getall(),
                                            'No of Ratings':resp.xpath("(//a[@class='pdp-link pdp-link_size_s pdp-link_theme_blue pdp-review-summary__link']/text())[1]").get(),
                                            'Store_url/dropship_supplier':absolute_url,
                                            'product_url':abcd,
                                            'image_url':img,
                                            'regular_price':dis,
                                            'sale_price':reg,
                                        }
                                    except:
                                        print("There is a error in the yield")   
                                except:
                                    print("There is a error in the product page")
                                driver.execute_script("window.history.go(-1)")
                                time.sleep(4)
                            else:
                                driver.execute_script("window.scrollTo(0, 1200)") 
                                time.sleep(3)

                    else:
                        print("pagination")   
                except:
                    print("Cannot get anything due to network loss")
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, 1200)") 
                time.sleep(2)
                driver.execute_script("window.scrollTo(1200, 2400)") 
                time.sleep(2)
                driver.execute_script("window.scrollTo(2400, 3600)") 
                time.sleep(2)
                driver.execute_script("window.scrollTo(3600, 4200)") 
                time.sleep(4)
                next = driver.find_element_by_xpath("//li[@title='Next Page']/a[@class='ant-pagination-item-link']")
                if next:
                    ActionChains(driver).move_to_element(next).click().perform()
                    next.click()
                    time.sleep(3)
                else:
                    print("There is a fault")
            else:
                print("There is no button left")
                n = 1
                break
