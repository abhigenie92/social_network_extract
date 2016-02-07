import time,os,sqlite3,pdb,random
from get_proxy import get_proxy_fastest
from pprint import pprint
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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


def return_html_code(url,use_proxy):    
    dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
    if use_proxy==True:
        proxy_address=random.choice(get_proxy_fastest())
        proxy_type='https'
        print proxy_address,proxy_type
        service_args = [
        '--proxy='+proxy_address,
        '--proxy-type='+proxy_type,
        ]
        driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=service_args)
    else:
        driver = webdriver.PhantomJS(desired_capabilities=dcap)     
    driver.maximize_window()
    driver.get(url)
    print 'Loading initial page'
    # initial wait for the tweets to load
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))
    except TimeoutException:
        print 'No tweets here'
        driver.quit()
        return False
    # scroll down to the last tweet until there is no more tweets loaded
    print 'Scrolling tweets'
    while True:       
        tweets = driver.find_elements_by_css_selector("li[data-item-id]")
        number_of_tweets = len(tweets)
        print(number_of_tweets)

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
    driver.quit()
    #with open("check.html",'w') as f: f.write(html_full_source)
    return html_full_source

if __name__ == '__main__':
    #url='https://twitter.com/search?q=Alcoholics%20Anonymous%20Drunk%20since%3A2011-01-24%20until%3A2011-02-23&src=typd&lang=en'
    url='https://twitter.com/search?q=wtf&src=typd&lang=en'
    return_html_code(url ,True)
