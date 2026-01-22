import os
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = None
    try:
        conn = pg2.connect(
            os.getenv("DATABASE_URL"),
            cursor_factory = RealDictCursor
        )
        yield conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise e
    finally:
        if conn:
            conn.close()
