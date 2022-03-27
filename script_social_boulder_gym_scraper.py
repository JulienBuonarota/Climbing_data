## imports
import tool_boulder_parser as tbp
import tool_gym_scraper as tgs
import tool_DB as tdb
import pickle
import logging

# Logger
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

hdlr = logging.FileHandler("script_social_boulder_gym_scraper.log", mode='a')
hdlr.setLevel("INFO")

str_format = '%(asctime)s - %(levelname)s - %(message)s'
frmt = logging.Formatter(fmt=str_format)

hdlr.setFormatter(frmt)
logger.addHandler(hdlr)

# DB info
DB_d = {"dbname": "ClimbingGymDB", "user": "climbing_data", "password": "admin", "host": "localhost"}
gyms = tdb.get_gym_table(DB_d)

# Scraping for each gym
for i, gym in gyms.iterrows():
    logger.info("Start scraping : {}".format(gym['name']))
    try:
        ## Get the boulder html
        j = 0
        while j < 2: # sometimes fails withtout good reason, trying again usually works
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
    except:
        logger.info("FAILED scraping : {}".format(gym['name']))
    else:
        logger.info("Succesfully scraped : {}".format(gym['name']))
