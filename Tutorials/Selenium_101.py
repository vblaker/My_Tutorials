from selenium import webdriver
import selenium.webdriver.common.keys

driver = selenium.webdriver.Chrome("D:\Google Drive\Continuous Education\Python\My_Tutorials\selenium_drivers\chromedriver.exe")
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()