from selenium import webdriver
from get_proxy import get_proxy_fastest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib,requests,unidecode,lxml,pdb,random
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
    vdisplay =Xvfb()
    vdisplay.start()
    proxy_address_list=get_proxy_fastest()
    if proxy_address_list !=False:
    	proxy_address=random.choice(proxy_address_list)
    	ip,port=proxy_address.split(':')
    	print ip,port
    	profile = webdriver.FirefoxProfile()
    	profile.set_preference("network.proxy.http", ip);
    	profile.set_preference("network.proxy.http_port", port);
    	profile.set_preference("network.proxy_type", 1);
    	driver=webdriver.Firefox(firefox_profile=profile)
    else:
        print "Using localhost, unable to get proxy"
	driver=webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)
    # initial wait for the tweets to load
    # initial wait for the tweets to load
    wait = WebDriverWait(driver, 30)
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))
    except TimeoutException:
        driver.quit()
        return False    # scroll down to the last tweet until there is no more tweets loaded
    while True:
        tweets = driver.find_elements_by_css_selector("li[data-item-id]")
        print len(tweets)  #added in edit 1
	number_of_tweets=len(tweets)
        driver.execute_script("arguments[0].scrollIntoView(true);", tweets[-1])
        try:
            wait.until(wait_for_more_than_n_elements_to_be_present((By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))
        except TimeoutException:
            break
    html_full_source=driver.page_source
    driver.close()
    vdisplay.stop()
    return html_full_source

if __name__ == '__main__':
    #url='https://twitter.com/search?q=Alcoholics%20Anonymous%20Drunk%20since%3A2011-01-24%20until%3A2011-02-23&src=typd&lang=en'
    url='https://twitter.com/search?q=wtf&src=typd&lang=en'
    return_html_code(url )
