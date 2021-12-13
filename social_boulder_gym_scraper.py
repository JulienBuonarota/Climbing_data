import requests_html as rh
import re

url = "https://www.sboulder.com/arkose/nation"

session = rh.HTMLSession()
r = session.get(url)

r.html.render(sleep=1)

boulders = r.html.xpath('//*[@class="card-card-tr-50"]', first=True)

raw_html = r.html.raw_html
raw_html = raw_html.decode()
boulder_regex = re.compile("card-card-tr")

found = boulder_regex.findall(raw_html)

## other way from requests-html website
r2 = session.get(url)
r2.html.render()
sel = '#react-root > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)'

print(r2.html.find(sel, first=True).text)

## other method using selenium browser
import helium as hel
import bs4
import re
url = "https://www.sboulder.com/arkose/nation"
# the use of the firefox browser needs geckodriver
# hel.Config.implicit_wait_secs = 20
browser = hel.start_firefox(url)
html = browser.page_source

soup = bs4.BeautifulSoup(html, 'html.parser')

#nee to scroll down the page
boulders = soup.find_all('div', {'class': 'card-card-tr-46'})


hel.kill_browser()

## Using selenium by hand
import selenium as sel
from selenium.webdriver.common.by import By
import time

url = "https://www.sboulder.com/arkose/nation"

driver = sel.webdriver.Firefox()
driver.get(url)

boulders = driver.find_elements_by_class_name('card-card-tr-46')

## Same as previous but with automated wait of element of class="card-dard-tr-46"
import selenium as sel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import bs4 as bs

url = "https://www.sboulder.com/arkose/nation"

# Headless firefox
# firefoxOptions = sel.webdriver.FirefoxOptions()
# firefoxOptions.headless = True
driver = sel.webdriver.Firefox()
# Loading the site, wait until boulder elements are in the html and then scroll down
driver.get(url)
try:
    # wait for boulders to load
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-card-tr-46')))
    # Once the first boulders are there, the page need to be scrolled down to get them all
    # html = driver.find_element_by_tag_name('html') # used to send keys to scroll down
    html = driver.find_element(By.TAG_NAME, 'html')
    bottom_page_reached = False
    while not bottom_page_reached:
        html.send_keys(Keys.END)
        time.sleep(1)
        # in social boulder (sb), when the bottom is reached, a button appear to see the taken down boulders
        sb_buttons = driver.find_elements(By.TAG_NAME, 'button')
        all_button_texts = "".join([i.text for i in sb_buttons])
        bottom_page_reached = bool(re.search('See taken down problems', all_button_texts))

finally:
    # get all the boulders
    page_source = bs.BeautifulSoup(driver.page_source, 'html.parser')
    boulders = page_source.find_all('div', {'class': 'card-card-tr-46'})
    driver.close()








