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
import time
from selenium.webdriver.common.action_chains import ActionChains
class ComputerAccessoriesSpider(scrapy.Spider):
    name = 'computer_Accessories'
    allowed_domains = ['www.lazada.com.my']
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.lazada.com.my/shop-software/?spm=a2o4k.pdp_revamp.breadcrumb.3.54b05c1aRaQ9f5",
            callback=self.parse,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'},
            dont_filter=True,
        )
    def parse(self, response):
        path = which("chromedriver")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) #if you want to see what's goging on uncomment this line and comment 4 lines below
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_argument("--headless")
        
        driver = webdriver.Chrome(executable_path=path,options=chrome_options)
        driver.get(response.url)
        time.sleep(3)
        try:
            btn_info_page = driver.find_elements_by_xpath("//div[@class='c16H9d']/a")
            if btn_info_page:
                for wsa in range(0,len(btn_info_page)):
                    # try:          
                    #     driver.execute_script("window.scrollTo(0, 1200)") 
                    #     time.sleep(2)
                    #     driver.execute_script("window.scrollTo(1200, 2400)") 
                    #     time.sleep(2)
                    #     driver.execute_script("window.scrollTo(2400, 3600)") 
                    #     time.sleep(2)
                    #     driver.execute_script("window.scrollTo(3600, 4200)") 
                    #     time.sleep(4)
                    # except:
                    #     print("cannot scroll page")
                    btn_info_page = driver.find_elements_by_xpath("//div[@class='c16H9d']/a")[wsa]
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
                print("pagination")   
        except:
            print("Cannot get anything due to network loss")