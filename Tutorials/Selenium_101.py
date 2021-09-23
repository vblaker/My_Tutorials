from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import selenium.webdriver.common.keys

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(by=By.NAME, value="q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
