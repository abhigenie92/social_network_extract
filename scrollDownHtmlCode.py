from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib,requests,unidecode,lxml,pdb,time
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

    # initial wait for the tweets to load
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))
    except TimeoutException:
        return False
    # scroll down to the last tweet until there is no more tweets loaded
    z=0
    num_rightnow=range(100,9500000,100)
    print "Scrolling tweets"
    while True:
        tweets = driver.find_elements_by_css_selector("li[data-item-id]")
        number_of_tweets = len(tweets)
        if number_of_tweets > num_rightnow[z]:
            print num_rightnow[z],
            z=z+1# move to the top and then to the bottom 5 times in a row
        # move to the top and then to the bottom 5 times in a row
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, 0)")
            driver.execute_script("arguments[0].scrollIntoView(true);", tweets[-1])
            time.sleep(0.5)

        try:
            wait.until(wait_for_more_than_n_elements_to_be_present((By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))
        except TimeoutException:
            break

    html_full_source=driver.page_source    
    driver.close()
    return html_full_source

	
