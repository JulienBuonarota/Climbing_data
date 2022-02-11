import psycopg2
import pandas

# def get_raw_table_list(DB_d, table_name):
#     with psycopg2.connect("dbname=ClimbingGymDB user=climbing_data password=admin host=localhost") as conn:
#         with conn.cursor() as cur:
#             cur.execute("""SELECT * FROM gym;""")
#             gyms = cur.fetchall()
#     return gyms

def parse_df_gym_list(gyms_raw):
    return df = pandas.DataFrame(gyms_raw, columns=['id', 'name', 'city', 'adress', 'url', 'scrape_on'])

    
