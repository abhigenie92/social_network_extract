from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib,requests,unidecode,lxml,pdb
from pyvirtualdisplay import Display
from xvfbwrapper import Xvfb
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
	print url
	vdisplay =Xvfb()
	vdisplay.start()
	driver = webdriver.Firefox()
	driver.maximize_window()
	driver.get(url)
	# initial wait for the tweets to load
	wait = WebDriverWait(driver, 240)
	wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))
	# scroll down to the last tweet until there is no more tweets loaded
	print "Scrolling to retrieve all tweets..."
	num_rightnow=range(100,9500000,100)
	z=1
	while True:
	    tweets = driver.find_elements_by_css_selector("li[data-item-id]")
	    number_of_tweets = len(tweets)
	    print number_of_tweets
	    if number_of_tweets > num_rightnow[z]:
	    	print num_rightnow[z],
	    	z=z+1
	    driver.execute_script("arguments[0].scrollIntoView(true);", tweets[-1])
	    try:
	        wait.until(wait_for_more_than_n_elements_to_be_present((By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))
	    except TimeoutException:
		try:
			wait.until(wait_for_more_than_n_elements_to_be_present((By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))
		except TimeoutException:
       			break
	print number_of_tweets       
	html_full_source=driver.page_source
	driver.close()
	vdisplay.stop()
	return html_full_source
	
