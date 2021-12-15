## Same as previous but with automated wait of element of class="card-dard-tr-46"
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

url = "https://www.sboulder.com/arkose/nation"

# Headless firefox
# firefoxOptions = sel.webdriver.FirefoxOptions()
# firefoxOptions.headless = True
driver = sel.webdriver.Firefox()
# Loading the site, wait until boulder elements are in the html and then scroll down
driver.get(url)

# wait for boulders to load
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'card-card-tr-46')))
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
boulders_source = []
# each boulder 'card' needs to be expanded to have access to the tag, date and image
boulders = driver.find_elements(By.CLASS_NAME, 'card-card-tr-46')
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
                EC.presence_of_element_located((By.CLASS_NAME, 'card-info-tr-58')))
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
    boulders_source.append(boulder_source)

    # a short sleep is necessary in order for the next button click to work
    # probably as to do with position update time
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

## temporary save of bouldres source html
import json
json.dump('ttt', boulders_source)
import pickle
with open('boulder_source.pckl', 'wb') as file:
    pickle.dump(boulders_source, file)
with open('boulder_source.pckl', 'rb') as file:
    boulders_source = pickle.load(file)

## boulder parser
import cssutils
"""
Retrieve : 
- [X] grade (color and number)
- [X] position in gym
- [X] tags
- [X] date added
- [X] nb points
- [X] nb completions
- [X] image
"""
def string_to_rgb(s: str) -> tuple:
    """
    Convert a string with rgb information into a tuple
    with the informations
    exemple of string ' rgb(0, 10, 0) '
    :param s: string to parse
    :return: tuple representing the rgb
    """
    r = re.compile('[0-9]+')
    m = r.findall(s)
    return tuple([int(i) for i in m])

def string_to_polyline_coord(s: str) -> tuple:
    """
    Convert a string with pairs of numbers
    example of string = '2,34 45,6'
    :param s: string to convert
    :return: tuple of arbitrary number of tuple (each pair)
    """
    r = re.compile('[1-9]+,[1-9]+')
    m = r.findall(s)
    pairs = [i.split(',') for i in m]
    return tuple([(int(i), int(j)) for i, j in pairs])

def tags_parser(s: str) -> tuple:
    """
    Retrieve the tag text out of a string of multiple tags delimited by #
    :param s: the sttring of # seperated words or expresionns
    :return: a tuple with the text of each tags
    """
    return tuple([i.strip() for i in s.split('#') if i != ''])

boulder_color_rgb = {"purple": (138, 43, 226), "black": (0, 0, 0), "red": (221, 0, 0),
                     "blue": (30, 136, 229), "green": (0, 128, 0), "yellow": (255, 235, 59)}
boulder_rgb_color = {v: k for k, v in boulder_color_rgb.items()}

boulder_num = 1
b = boulders_source[boulder_num]
## Grade =  color + number
grade_scale = b.find_all('svg', {'class': 'cardHeader-labelIcon-tr-10'})
# the grade color is in the style of the second svg
style = cssutils.parseStyle(grade_scale[1]['style'])
grade_rgb = string_to_rgb(style['fill'])
grade_color = boulder_rgb_color[grade_rgb]
grade_value = grade_scale[1]['filled']

## Gym map
map = b.find('g', {'stroke-linecap': 'butt'})
map_sections = map.find_all('polyline')
map_sections_positions = [string_to_polyline_coord(i['points']) for i in map_sections]

## Position of boulder in the gym
map = b.find('g', {'stroke-linecap': 'butt'})
map_section = map.find('polyline', {'style': 'opacity: 1;'})
map_section_position = string_to_polyline_coord(map_section['points'])

## Number of points and number of time completed
points_and_completion = b.find('div', {'class': 'cardHeader-points-tr-20'}).text
points, completion = [int(i) for i in points_and_completion.split('pts')]

# points_and_completion = b.find('div', {'class': 'cardHeader-points-tr-20'})
# points_and_completion_text = [i.text for i in points_and_completion.find_all('div')]
# points = int(points_and_completion_text[0].split('pts')[0])
# completion = int(points_and_completion_text[1])
## Tags, date and image
boulder_source = b
# get the date and tags
infos = boulder_source.find_all('div', {'class': 'card-info-tr-58'})
infos_text = [i.text for i in infos]
# Infos cn catch several other elements representing likes, comments,...
# search of element that match a date format
date_regex = re.compile('\d+-\d+-\d+')
date_index = [bool(re.match(date_regex, i)) for i in infos_text].index(True)
date = infos_text[date_index]
# search element matching tags format
tags_index = [bool(re.match('#[a-zA-Z]+', i)) for i in infos_text].index(True)
tags = tags_parser(infos_text[tags_index])
# get the image
image_url = boulder_source.find('img', {'class': 'card-image-tr-41'})['src']
local_filename, headers = urllib.request.urlretrieve(image_url, "./images/1.jpg")
# Get the likes and comments, if there is some (otherwise not displayed)
like_svg_path = "M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 " \
                 "14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
comment_svg_path = "M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18zM18 " \
                   "14H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"
likes = 0
comments = 0
for count, info in enumerate(infos):
    svg_path = info.find('path')['d']
    if svg_path == like_svg_path:
        likes = int(infos[count].text)
    elif svg_path == comment_svg_path:
        comments = int(infos[count].text)

## Verification of script
print("""
Boulder number {}
- grade (color and number) {} {}
- position in gym {}
- tags {}
- date added {}
- likes {}
- comments {}
- nb points {}
- nb completions {}
- image {}
""".format(boulder_num, grade_color, grade_value, map_section_position, tags, date, likes, comments, points, completion, image_url))
##
# TODO the number of completion and likes appear next to the date which change the html hierarchy, but not if they are 0
#  the date and tags retrieval need to take it into account
