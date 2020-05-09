import time
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class Searching :
    def __init__(self,search):
        self.search = search
        self.driver = webdriver.Chrome(ChromeDriverManager().install()) 
    def fill(self):
        self.driver.get("https://www.Google.com/")
        while True:
            try:
                self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(self.search + Keys.ENTER)
                break
            except:
                time.sleep(0.01)