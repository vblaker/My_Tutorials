import time
from selenium import webdriver

# Optional argument, if not specified will search path.
driver = webdriver.Chrome('D:\Google Drive\Continuous Education\Python\Tutorials\selenium_drivers\chromedriver.exe')
driver.get('http://www.google.com/')

# Let the user actually see something!
time.sleep(5)

search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()

# Let the user actually see something!
time.sleep(5)
driver.quit()
