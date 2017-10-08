from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.wait = WebDriverWait(driver, 5)
driver.get("https://www.google.com/")


search_box = driver.find_element_by_xpath('//*[@id="lst-ib"]')
search_box.send_keys("do a barrel roll", Keys.ENTER) # Or whatever you want to fill the text box with

time.sleep(5)

driver.quit()
