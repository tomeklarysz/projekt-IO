import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

DB_NAME = os.getenv("DB_NAME") 
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS") 
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    """Establishes and returns a database connection."""
    if not all([DB_NAME, DB_USER, DB_PASS]):
        print("Error: Please set DB_NAME, DB_USER, and DB_PASS in the .env file.")
        return None
    
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print(f"PostgreSQL connection error: {error}")
        print("Ensure the PostgreSQL server is running and the database is created!")
        return None

def create_tables(conn):
    """Creates the 'employees' and 'verification_statuses' tables with final requested fields."""
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                qr_hash VARCHAR(256) UNIQUE NOT NULL, 
                vector_features DOUBLE PRECISION[], 
                photo_path VARCHAR(255)
            );
        """)
        print("Table 'employees' created successfully.")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS verification_statuses (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
                is_confirmed BOOLEAN NOT NULL
            );
        """)
        print("Table 'verification_statuses' created successfully.")

        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error during table creation: {error}")
        conn.rollback()
    finally:
        cur.close()

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        create_tables(conn)
        conn.close()