# -*- coding: utf-8 -*-
from helper_class import *

class INTERFACING():

    def __init__(self,drivertype,driver_path):
        self.drivertype = drivertype
        self.driver_path = driver_path
        self.driver_initialized = False
        self.driver = ''
        # self.headless = headless
        
    def get_url_response(self,url):   

        while 1:
            try:
                print("Processing URL: " , url,)
                agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
                html = requests.get(url,headers=agent).text
                return html
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)


    def make_soup(self):
        return BeautifulSoup(self.driver.page_source, 'lxml')

    def make_soup_url(self,page_url):
        return BeautifulSoup(self.get_url_response(page_url), 'lxml')

    def current_url(self):
        return self.driver.current_url

    def get_user_agent(self):
        useragents = [
                        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                         'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
                         'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
                         'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
                         'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
                         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
                         'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                         'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
                         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
                     ]

        user_agent = random.choice(useragents)
        
        return 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'

    def get_driver(self):
        
        if self.drivertype == "Chrome":
            from selenium.webdriver.chrome.options import Options
            if self.driver_path is '':
                raise Exception("Driverpath cannot be blank for Chrome")

            opts = Options()
            current_ua = self.get_user_agent()
            print("Current UA: " , current_ua)
            opts.add_argument("user-agent=%s" % current_ua)
            # if self.headless:
            #     opts.add_argument("--headless")
            opts.add_argument("--disable-gpu")
            opts.add_argument("--disable-notifications")
            opts.add_argument("--start-maximized")

            self.driver = webdriver.Chrome(self.driver_path, options=opts)
            self.driver_initialized = True

        elif self.drivertype== 'Firefox':
            from selenium.webdriver.firefox.options import Options
            opts = Options()
            # if self.headless:
            #     opts.add_argument("--headless")
            print(self.driver_path)
            self.driver = webdriver.Firefox(executable_path=self.driver_path, options=opts)
            self.driver_initialized = True

        else:   
            raise Exception("Invalid Driver Type:" + self.drivertype)

    def close_driver(self):

        if self.driver_initialized:
            self.driver.quit()
            print("Closed the driver")
            self.driver_initialized = False

    def get_selenium_response(self,url):
        page_src = None
        try:
            if not self.driver_initialized:
                self.get_driver()
            else:
                print("Driver Already Initialized")

            print("Processing URL: ", url)
            self.driver.get(url)
            sleep_time = 3
            print("Automated Browser takes sometime to get ready, so implicitly sleeping for " + str(sleep_time) + " seconds")
            time.sleep(sleep_time)
            
        except NoSuchElementException as error:
            print(error)
            self.driver_initialized = False
            self.close_driver()
            return False

        except ElementClickInterceptedException as error:
            print (error)
            self.driver_initialized = False
            self.close_driver()
            return False

        except TimeoutException as error:
            print(error)
            self.driver_initialized = False
            self.close_driver()
            return False

        return self.make_soup()

    def get_page_source(self):
        return self.driver.page_source

    def clicking(self,xpath):
        elem = self.driver.find_element_by_xpath(xpath)
        elem.click()
        time.sleep(random.randint(2,3))

    def entering_values(self,xpath,value):
        elem = self.driver.find_element_by_xpath(xpath)
        elem.clear()
        elem.send_keys(value)
        time.sleep(random.randint(2,4))

