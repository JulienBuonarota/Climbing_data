## imports
import boulder_parser as bp
import gym_scraper as gs

## Get the boulder html
url = "https://www.sboulder.com/arkose/nation"
boulders_source = gs.boulder_scraper(url)
## Parse the html
parsed_boulder_list = [bp.boulder_parser(b) for b in boulders_source]

## temporary save of bouldres source html
import pickle
# with open('parsed_boulder_list.pckl', 'wb') as file:
#     pickle.dump(parsed_boulder_list, file)

with open('parsed_boulder_list.pckl', 'rb') as file:
    boulders_source = pickle.load(file)

import psycopg2

with psycopg2.connect("dbname=gym_arkose_nation user=climbing_data password=admin host=localhost") as conn:
    with conn.cursor() as cur:


# with open('boulder_source.pckl', 'rb') as file:
#     boulders_source = pickle.load(file)

# TODO Storage of the parsed boulders in a database

