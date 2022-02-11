 import psycopg2

# cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# boulders table
# grade 
with psycopg2.connect("dbname=ClimbingGymDB user=climbing_data password=admin host=localhost") as conn:
    # boulder table
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS boulder 
        (id serial PRIMARY KEY,
        grade text,
        sub_grade text,
        gym_id smallint,
        map_section path,
        tag text[],
        date_opened date,
        date_closed date,
        nb_like smallint,
        nb_comment smallint,
        nb_point smallint,
        nb_completion smallint,
        img_url text);""")
    # gym table
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS gym
        (id serial PRIMARY KEY,
        gym_name text,
        city text,
        address text,
        social_boulder_url text,
        scrape_on boolean);""")
    # Index
    with conn.cursor() as cur:
        cur.execute("""CREATE INDEX IF NOT EXISTS gym_id_idx
                       ON boulder (gym_id);""")

        
  
