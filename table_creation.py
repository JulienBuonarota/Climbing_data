import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect("dbname=gym_arkose_nation user=climbing_data password=admin host=localhost")

# Open a cursor to perform database operations
cur = conn.cursor()

# create table and insert data
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

conn.commit()

# test with
with conn.cursor() as cur:
    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

with psycopg2.connect("dbname=gym_arkose_nation user=climbing_data password=admin host=localhost") as connn:
    with connn.cursor() as curr:
        curr.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (10222, "abc'def"))
    with connn.cursor() as curr:
        curr.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (1302, "abc'def"))
# closing connection
cur.close()
conn.close()

# boulders table
# grade 
with psycopg2.connect("dbname=gym_arkose_nation user=climbing_data password=admin host=localhost") as conn:
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE Boulders 
        (id serial PRIMARY KEY,
        grade text,
        sub_grade smallint,
        map_section path,
        tags text[],
        date_opened date,
        likes smallint,
        comments text[],
        points smallint,
        nb_completions smallint,
        img_url text);""")
