import selenium as sel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as sel_exceptions
from selenium.webdriver.common.keys import Keys
import time
import re
import bs4 as bs
import urllib.request

# TODO define a logger to display the prints when debugging only

def boulder_scraper(url):
    """
    Scrape all opened boulders at url.
    :param: url
    :return: list of boulder html
    """
    # Headless firefox
    firefoxOptions = sel.webdriver.FirefoxOptions()
    firefoxOptions.headless = True
    driver = sel.webdriver.Firefox(options=firefoxOptions)
    # Loading the site, wait until boulder elements are in the html and then scroll down
    driver.get(url)
    # wait for boulders to load
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-card-tr-47')))
    # Once the first boulders are there, the page need to be scrolled down to get them all
    html = driver.find_element(By.TAG_NAME, 'html')
    bottom_page_reached = False
    while not bottom_page_reached:
        html.send_keys(Keys.END)
        # in social boulder (sb), when the bottom is reached, a button appear to see the taken down boulders
        sb_buttons = driver.find_elements(By.TAG_NAME, 'button')
        all_button_texts = "".join([i.text for i in sb_buttons])
        bottom_page_reached = bool(re.search('See taken down problems', all_button_texts))

    # Open and store all boulder 'card'
    boulder_list = []
    # each boulder 'card' needs to be expanded to have access to the tag, date and image
    boulders = driver.find_elements(By.CLASS_NAME, 'card-card-tr-47')
    # It is necessary to scroll back up the page to be able to click on the buttons
    driver.execute_script("window.scrollTo(0, 0)")
    for count, boulder in enumerate(boulders):
        print("{}/{}".format(count, len(boulders)))
        # get the boulder unique name
        name = boulder.find_element(By.TAG_NAME, 'div').get_attribute('name')
        # find the expand button and click it to open it, will try a maximum of 3 times
        for i in range(3):
            button = boulder.find_element(By.XPATH,
                                         "//div[@name='{}']/span/div/div[6]/div".format(name))
            sel.webdriver.ActionChains(driver).click(button).perform()
            # wait for the tags to load,
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'card-info-tr-59')))
            except sel_exceptions.TimeoutException:
                print("The boulder 'card' didn't opened at boulder {}/{} after {} clicks"
                      .format(count, len(boulders), i+1))
            else:
                break
            # Maximum number of try reached
            if i == 2:
                raise Exception("Unable to open boulder card and thus get the proper html content")

        # get the source html for the complete boulder
        boulder_source = boulder.get_attribute('innerHTML')
        boulder_source = bs.BeautifulSoup(boulder_source, 'html.parser')
        boulder_list.append(boulder_source)

        # a short sleep is necessary in order for the next button click to work
        # probably has to do with position update time
        time.sleep(0.3)
        # find the expand button and click it to close it, will try a maximum of 3 times
        for i in range(3):
            sel.webdriver.ActionChains(driver).click(button).perform()
            # wait for the tags earlier retrieve to disappear from the page
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.invisibility_of_element(element))
            except sel_exceptions.TimeoutException:
                print("The boulder 'card' didn't closed at boulder {}/{} after {} clicks"
                      .format(count, len(boulders), i + 1))
            else:
                break
            # Maximum number of try reached
            if i == 2:
                raise Exception("Unable to close boulder card and thus get the proper html content")
    driver.quit()
    # return all the boulder html
    return boulder_list
