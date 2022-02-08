import psycopg2

# cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# boulders table
# grade 
with psycopg2.connect("dbname=gym_arkose_nation user=climbing_data password=admin host=localhost") as conn:
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
        num_like smallint,
        num_comment smallint,
        point smallint,
        completion smallint,
        img_url text);""")
    # comments table
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS comment
        (id serial PRIMARY KEY,
        boulder_id integer,
        added_date date,
        comment text);""")
    # gym table
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS gym
        (id serial PRIMARY KEY,
        city text,
        address text);""")

    with conn.cursor() as cur:
        cur.execute("""CREATE INDEX IF NOT EXISTS comment_idx
                       ON comment (boulder_id);""")
    with conn.cursor() as cur:
        cur.execute("""CREATE INDEX IF NOT EXISTS gym_id_idx
                       ON boulder (gym_id);""")

        
