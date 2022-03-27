import pickle
import psycopg2
import tool_gym_parser as tgp
import pandas

def get_raw_table_list(DB_d):
    with psycopg2.connect("dbname=ClimbingGymDB user=climbing_data password=admin host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM gym;""")
            gyms = cur.fetchall()
    return gyms

def parse_df_gym_list(gyms_raw):
    return pandas.DataFrame(gyms_raw, columns=['id', 'name', 'city', 'adress', 'url', 'scrape_on'])

def get_gym_table(DB_d):
    return parse_df_gym_list(get_raw_table_list(DB_d))

def feed_DB(DB_d, gym, boulders_source):
    conn = psycopg2.connect("dbname={} user={} password={} host={}".format(*[i for i in DB_d.values()]))
    try:
        for data in boulders_source:
            # insert image
            with conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("""
                        INSERT INTO gym_image(gym_id, img_url, os_path_to_img)
                        VALUES (%s, %s, %s);""",
                                    (int(gym["id"]), data["img_url"], None))
                    except psycopg2.errors.UniqueViolation:
                        print('gym_image table unique constraint violation')
            # insert map section
            with conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("""
                        INSERT INTO gym_map_section(gym_id, map_section)
                        VALUES (%s, %s);""",
                                    (int(gym["id"]), str(data["map_section"])))
                    except psycopg2.errors.UniqueViolation:
                        print("gym_map_section table unique constraint violation")
            # insert into boulder table
            with conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("""
                        INSERT INTO boulder(grade, sub_grade, gym_id, map_section_id, tag, date_opened, date_closed, img_id)
                        VALUES (%s, %s, %s,
                               (SELECT id FROM gym_map_section WHERE gym_map_section.gym_id = %s AND gym_map_section.map_section = %s),
                               %s, %s, %s,
                               (SELECT id FROM gym_image WHERE gym_image.gym_id = %s AND gym_image.img_url = %s));""",
                                    (data["grade"][0], data["grade"][1], int(gym["id"]),
                                     int(gym["id"]), str(data["map_section"]),
                                     "{" + ", ".join(data["tags"]) + "}", data["date_opened"], None,
                                     int(gym["id"]), data["img_url"]))
                    except psycopg2.errors.UniqueViolation:
                        print("boulder table unique constraint violation")
            # get boulder id
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    SELECT id
                    FROM boulder
                    WHERE
                    	grade = %s
                    	AND sub_grade = %s
                    	AND gym_id = %s
                    	AND map_section_id = (SELECT id FROM gym_map_section WHERE gym_map_section.gym_id = %s AND gym_map_section.map_section = %s)
                    	AND tag = %s
                    	AND date_opened = %s
                    	AND img_id = (SELECT id FROM gym_image WHERE gym_image.gym_id = %s AND gym_image.img_url = %s);""",
                                (data["grade"][0], data["grade"][1], int(gym["id"]), int(gym["id"]),
                                 str(data["map_section"]), "{" + ", ".join(data["tags"]) + "}",
                                 data["date_opened"], int(gym["id"]), data["img_url"]))
                    boulder_id = cur.fetchall()[0][0]
            # get todays date
            import datetime
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # insert nb_likes
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    INSERT INTO boulder_like(boulder_id, registration_date, nb_like)
                    VALUES (%s, %s, %s);""",
                                (boulder_id, now, data["likes"]))
            # insert nb_comment
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    INSERT INTO boulder_comment(boulder_id, registration_date, nb_comment)
                    VALUES (%s, %s, %s);""",
                                (boulder_id, now, data["comments"]))
            # insert nb_point
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    INSERT INTO boulder_point(boulder_id, registration_date, nb_point)
                    VALUES (%s, %s, %s);""",
                                (boulder_id, now, data["points"]))
            # insert nb_completion
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    INSERT INTO boulder_completion(boulder_id, registration_date, nb_completion)
                    VALUES (%s, %s, %s);""",
                                (boulder_id, now, data["completion"]))
    finally:
        conn.close()
