import pickle
import psycopg2

DB_d = {"dbname": "ClimbingGymDB", "user": "climbing_data", "password": "admin", "host": "localhost"}

with open('parsed_boulder_list.pckl', 'rb') as file:
    boulders_source = pickle.load(file)


with psycopg2.connect("dbname={} user={} password={} host={}".format(*[i for i in DB_d.values()])) as conn:
    # boulder table
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO boulder(grade, sub_grade, gym_id, map_section, tag, date_opened, date_closed, nb_like, nb_comment, point, nb_completion, img_url)
        VALUES (%s, %s, %s, CAST(%s AS PATH), %s, %s, %s, %s, %s, %s, %s, %s);""",
                    ('purple', '2', 1, '((62, 46), (73, 46), (73, 52))',
                     '{"100%\xa0Volumes", "Powerful"}', '2021-12-21', None, 0, 0, 700, 0,
                     'https://socialboulder.s3-eu-west-1.amazonaws.com/800/bouldersPics/cycKwGkY3oeqBPtpK.jpg'))
