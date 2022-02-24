## imports
import tool_boulder_parser as tbp
import tool_gym_scraper as tgs
import tool_DB as tdb
import pickle

DB_d = {"dbname": "ClimbingGymDB", "user": "climbing_data", "password": "admin", "host": "localhost"}
gyms = tdb.get_gym_table(DB_d)

for i, gym in gyms.iterrows():
    ## Get the boulder html
    j = 0
    while j < 2:
        try:
            boulders_source = tgs.boulder_scraper(gym["url"])
            j = 2
        except:
            print("try {} failed".format(i))
            j = j + 1
    ## Parse the html
    parsed_boulder_list = [tbp.boulder_parser(b) for b in boulders_source]
    ## Save to DB
    tdb.feed_DB(DB_d, gym, parsed_boulder_list)
