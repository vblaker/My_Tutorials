from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome("D:\Google Drive\Continuous Education\Python\My_Tutorials\selenium_drivers\chromedriver.exe")

driver.set_page_load_timeout(10)
driver.get("http://google.com")
driver.find_element_by_name("q").send_keys("Selenium automation")
driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
time.sleep(10)
driver.quit()
