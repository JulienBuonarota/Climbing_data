import psycopg2

# cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# boulders table
# grade 
with psycopg2.connect("dbname=ClimbingGymDB user=climbing_data password=admin host=localhost") as conn:
    # gym table
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS gym
        (id serial PRIMARY KEY,
        gym_name text,
        city text,
        address text,
        social_boulder_url text,
        scrape_on boolean);""")
    # map section table
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS gym_map_section
        (id serial PRIMARY KEY,
        gym_id int REFERENCES gym(id),
        map_section text,
        UNIQUE(gym_id, map_section));""")
   # image table
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS gym_image
        (id serial PRIMARY KEY,
        gym_id int REFERENCES gym(id),
        img_url text,
        os_path_to_img text,
        UNIQUE(gym_id, img_url));""")
    # boulder table
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS boulder 
        (id serial PRIMARY KEY,
        grade text,
        sub_grade text,
        gym_id int REFERENCES gym(id),
        map_section_id int REFERENCES gym_map_section(id),
        tag text[],
        date_opened date,
        date_closed date,
        img_id int REFERENCES gym_image(id),
        UNIQUE(grade, sub_grade, gym_id, map_section_id, tag, date_opened, img_id));""")
    # nb like register
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS boulder_like
        (id serial PRIMARY KEY,
        boulder_id int REFERENCES boulder(id),
        registration_date date,
        nb_like int);""")
    # nb comment register
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS boulder_comment
        (id serial PRIMARY KEY,
        boulder_id int REFERENCES boulder(id),
        registration_date date,
        nb_comment int);""")
    # nb point register
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS boulder_point
        (id serial PRIMARY KEY,
        boulder_id int REFERENCES boulder(id),
        registration_date date,
        nb_point int);""")
    # nb completion register
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS boulder_completion
        (id serial PRIMARY KEY,
        boulder_id int REFERENCES boulder(id),
        registration_date date,
        nb_completion int);""")
    # Index
    with conn.cursor() as cur:
        cur.execute("""CREATE INDEX IF NOT EXISTS gym_id_idx
                       ON boulder (gym_id);""")


