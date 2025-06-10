import psycopg2
import json
def create():
	# Connect to the PostgreSQL database
	conn = psycopg2.connect(
	    dbname="test",
	    user="postgres",
	    password="postgres",
	    host="localhost",
	    port=5432
	)

	cur = conn.cursor()

	# Create a table with name, description, and url
	cur.execute("""
	    CREATE TABLE IF NOT EXISTS data (
	        id SERIAL PRIMARY KEY,
	        name TEXT NOT NULL,
	        description TEXT,
	        url TEXT,
	        poster TEXT
	    )
	""")


	# Commit and close
	conn.commit()
	cur.close()
	conn.close()

	print("Table 'data' with name, description, and url created successfully.")
def insert(name, description,url,poster):
	conn = psycopg2.connect(
	    dbname="test",
	    user="postgres",
	    password="postgres",
	    host="localhost",
	    port=5432
	)

	cur = conn.cursor()

	# Insert query
	cur.execute("""
	    INSERT INTO data (name, description, url,poster)
	    VALUES (%s, %s, %s,%s)
	""", (name, description, url,poster))

	# Commit and close
	conn.commit()
	cur.close()
	conn.close()

	print(f"✅ Data inserted into 'users' table. {name}, {description}, {url} , {poster}")


def getinfo():
	# Connect to the database
	conn = psycopg2.connect(
	    dbname="test",
	    user="postgres",
	    password="postgres",
	    host="localhost",
	    port=5432
	)

	cur = conn.cursor()

	# Fetch all rows
	cur.execute("SELECT id, name, description, url , poster  FROM data")
	rows = cur.fetchall()

	# Format as list of dicts
	data = []
	for row in rows:
	    data.append({
	        "id": row[0],
	        "name": row[1],
	        "description": row[2],
	        "url": row[3],
	        "poster": row[4]
	    })

	# Convert to JSON string
	json_data = json.dumps(data, indent=4)

	return json_data

	cur.close()
	conn.close()

def insert_url_and_poster(url, poster):
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO data (name, description, url, poster)
        VALUES (NULL, NULL, %s, %s)
        RETURNING id;
    """, (url, poster))

    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ URL and Poster added with ID {user_id}")
    return user_id

def update_name_and_description(user_id, name, description):
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cur = conn.cursor()

    cur.execute("""
        UPDATE data
        SET name = %s, description = %s
        WHERE id = %s;
    """, (name, description, user_id))

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Name and Description updated for ID {user_id}")

def delete_table():
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS data")
insert("1","2","3","4")