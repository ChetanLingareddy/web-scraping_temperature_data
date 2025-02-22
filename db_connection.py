import psycopg2

# Database connection settings
DB_NAME = "webscraping_db"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"
# Function to connect to PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print(" Successfully connected to PostgreSQL!")
        return conn
    except Exception as e:
        print("Database Connection Failed:", e)
        return None

# Function to create the table if it doesn't exist
def create_table():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
                id SERIAL PRIMARY KEY,
                temperature TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Table created (if not already present).")