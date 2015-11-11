from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib,requests,unidecode,lxml

class wait_for_more_than_n_elements_to_be_present(object):
    def __init__(self, locator, count):
        self.locator = locator
        self.count = count

    def __call__(self, driver):
        try:
            elements = EC._find_elements(driver, self.locator)
            return len(elements) > self.count
        except StaleElementReferenceException:
            return False

def return_html_code(url):
	driver = webdriver.Firefox()
	driver.maximize_window()
	driver.get(url)
	# initial wait for the tweets to load
	wait = WebDriverWait(driver, 10)
	wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))
	# scroll down to the last tweet until there is no more tweets loaded
	while True:
	    tweets = driver.find_elements_by_css_selector("li[data-item-id]")
	    number_of_tweets = len(tweets)
	    print number_of_tweets
	    driver.execute_script("arguments[0].scrollIntoView();", tweets[-1])
	    try:
	        wait.until(wait_for_more_than_n_elements_to_be_present((By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))
	    except TimeoutException:
	        break
	html_full_source=driver.page_source
	driver.close()
	return html_full_source
	