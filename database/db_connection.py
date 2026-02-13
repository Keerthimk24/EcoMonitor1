import psycopg2
from psycopg2 import sql

# Database Configuration
DB_CONFIG = {
    'dbname': 'environment_db',
    'user': 'postgres',
    'password': 'KEERTHI',  # CHANGE THIS to your actual password
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        
        # Create image_results table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS image_results (
                id SERIAL PRIMARY KEY,
                datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                image_name TEXT,
                pollution_level TEXT
            );
        """)
        
        # Create report_results table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS report_results (
                id SERIAL PRIMARY KEY,
                datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                report_text TEXT,
                issue_type TEXT
            );
        """)
        
        # Create aqi_results table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS aqi_results (
                id SERIAL PRIMARY KEY,
                datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                predicted_aqi FLOAT
            );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Tables created successfully.")
    else:
        print("Failed to create tables.")

if __name__ == "__main__":
    # Create the database if it doesn't exist (this part might require a connection to 'postgres' db first)
    try:
        temp_config = DB_CONFIG.copy()
        db_name = temp_config.pop('dbname')
        temp_config['dbname'] = 'postgres'
        
        conn = psycopg2.connect(**temp_config)
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' created.")
        
        cur.close()
        conn.close()
        
        create_tables()

    except Exception as e:
        print(f"Database setup error: {e}")
