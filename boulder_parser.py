import re
import urllib.request
import cssutils

"""
Tools and main function to parse boulder html
Get all this informations : 
- grade (color and number)
- position in gym
- tags
- date added
- likes
- comments
- nb points
- nb completions
- image
"""
# TODO create a gym object to store specific values, like grade colors
boulder_color_rgb = {"purple": (138, 43, 226), "black": (0, 0, 0), "red": (221, 0, 0),
                     "blue": (30, 136, 229), "green": (0, 128, 0), "yellow": (255, 235, 59)}
boulder_rgb_color = {v: k for k, v in boulder_color_rgb.items()}

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


def boulder_parser(boulder_html):
    ## Grade =  color + number
    grade_scale = boulder_html.find_all('svg', {'class': 'cardHeader-labelIcon-tr-10'})
    # the grade color is in the style of the second svg
    style = cssutils.parseStyle(grade_scale[1]['style'])
    grade_rgb = string_to_rgb(style['fill'])
    grade_color = boulder_rgb_color[grade_rgb]
    grade_value = grade_scale[1]['filled']

    ## Gym map
    map = boulder_html.find('g', {'stroke-linecap': 'butt'})
    map_sections = map.find_all('polyline')
    map_sections_positions = [string_to_polyline_coord(i['points']) for i in map_sections]

    ## Position of boulder in the gym
    map = boulder_html.find('g', {'stroke-linecap': 'butt'})
    map_section = map.find('polyline', {'style': 'opacity: 1;'})
    map_section_position = string_to_polyline_coord(map_section['points'])

    ## Number of points and number of time completed
    points_and_completion = boulder_html.find('div', {'class': 'cardHeader-points-tr-20'}).text
    points, completion = [int(i) for i in points_and_completion.split('pts')]

    ## Tags, date and image
    # get the date and tags
    infos = boulder_html.find_all('div', {'class': 'card-info-tr-58'})
    infos_text = [i.text for i in infos]
    # Infos cn catch several other elements representing likes, comments,...
    # search of element that match a date format
    date_regex = re.compile('\d+-\d+-\d+')
    date = None
    try:
        date_index = [bool(re.match(date_regex, i)) for i in infos_text].index(True)
    except ValueError:
        print("No matching while looking for dates in ", infos_text)
    else:
        date = infos_text[date_index]
    # search element matching tags format
    tags = None
    try:
        tags_index = [bool(re.search('#', i)) for i in infos_text].index(True)
    except ValueError:
        print("No matching while looking for tags in ", infos_text)
        print([bool(re.match('#', i)) for i in infos_text])
    else:
        tags = tags_parser(infos_text[tags_index])
    # get the image
    image_url = boulder_html.find('img', {'class': 'card-image-tr-41'})['src']
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

    return {'grade': (grade_color, grade_value), 'map_section': map_section_position, "tags": tags, "date_opened": date,
            "likes": likes, "comments": comments, "points": points, "completion": completion, "img_url": image_url}
