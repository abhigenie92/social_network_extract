from selenium.webdriver import ActionChains
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
    dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"

    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.maximize_window()

    driver.get(url)

    actions = ActionChains(driver)

    # initial wait for the tweets to load
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))
    # scroll down to the last tweet until there is no more tweets loaded
    # scroll down to the last tweet until there is no more tweets loaded
    print "Scrolling to retrieve all tweets..."
    num_rightnow=range(100,9500000,100)
    while True:
        tweets = driver.find_elements_by_css_selector("li[data-item-id]")
        number_of_tweets = len(tweets)
        if number_of_tweets > num_rightnow[z]:
	    print num_rightnow[z],
	    z=z+1
        # move to the last tweet
        driver.execute_script("arguments[0].scrollIntoView(true);", tweets[-1])
        actions.move_to_element(tweets[-1]).perform()

        try:
            wait.until(wait_for_more_than_n_elements_to_be_present((By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))
        except TimeoutException:
            break
    html_full_source=driver.page_source    
    driver.close()
    return html_full_source

	
