from selenium import webdriver
from selenium.webdriver.common.by import By

# Optional argument, if not specified will search path


def test_ice_spirit_displayed():
    driver = webdriver.Chrome()

    # 1. go to statsroyale.com
    driver.get('https://statsroyale.com')

    # 2. go to cards page
    driver.find_element(By.CSS_SELECTOR, "[href='/cards']").click()

    # 3. asset Ice Spirit is displayed
    ice_spirit_card = driver.find_element(By.CSS_SELECTOR, "[href*='Ice+Spirit']")
    assert ice_spirit_card.is_displayed
