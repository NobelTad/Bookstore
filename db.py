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
	        name TEXT ,
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
	cur.execute("SELECT id, name, description, url , poster FROM data ORDER BY id ASC")
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
def insert_book(name, description, url, poster):
    if not all([name, description, url, poster]):
        raise ValueError("All fields (name, description, url, poster) must be provided and non-empty")

    try:
        conn = psycopg2.connect(
            dbname="test",  # change if needed
            user="postgres",    # your username
            password="postgres",  # replace with actual
            host="localhost",   # or your host IP
            port="5432"         # default PostgreSQL port
        )
        cur = conn.cursor()
        query = """
        INSERT INTO data (name, description, url, poster)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        cur.execute(query, (name, description, url, poster))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id

    except Exception as e:
        print("Insert failed:", e)
        return None
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
def getrows(): 
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
    cur.execute("SELECT id, name, description, url, poster FROM data")
    rows = cur.fetchall()

    # Get number of rows
    num_rows = len(rows)

    cur.close()
    conn.close()

    return num_rows
print(getrows())