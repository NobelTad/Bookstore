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
	        url TEXT
	    )
	""")

	# Commit and close
	conn.commit()
	cur.close()
	conn.close()

	print("Table 'data' with name, description, and url created successfully.")
def insert(name, description,url):
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
	    INSERT INTO data (name, description, url)
	    VALUES (%s, %s, %s)
	""", (name, description, url))

	# Commit and close
	conn.commit()
	cur.close()
	conn.close()

	print(f"✅ Data inserted into 'users' table. {name}, {description}, {url} ")


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
	cur.execute("SELECT id, name, description, url FROM data")
	rows = cur.fetchall()

	# Format as list of dicts
	data = []
	for row in rows:
	    data.append({
	        "id": row[0],
	        "name": row[1],
	        "description": row[2],
	        "url": row[3]
	    })

	# Convert to JSON string
	json_data = json.dumps(data, indent=4)

	return json_data

	cur.close()
	conn.close()