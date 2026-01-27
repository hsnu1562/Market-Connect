import os
import psycopg2 as pg2
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env file

CREATE_TABLES_SQL = """
-- 1. Users Table (Stores Line info and Reputation)
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    line_uid VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    category VARCHAR(50), -- What do they sell?
    reputation_score INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Stalls Table (The Physical Locations)
CREATE TABLE IF NOT EXISTS stalls (
    stall_id SERIAL PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    lat DECIMAL(9,6),                       -- Latitude for map
    long DECIMAL(9,6),                      -- Longitude for map
    facilities TEXT,                        -- e.g., "Electricity, Water"
    owner_id INTEGER                        -- In real life, you'd link this to an Admin table
);
-- 3. Slots Table (The Inventory - Time Slots)
CREATE TABLE IF NOT EXISTS slots (
    slot_id SERIAL PRIMARY KEY,
    stall_id INTEGER REFERENCES stalls(stall_id), -- Foreign Key: Links to Stalls table
    date DATE NOT NULL,
    price INTEGER NOT NULL,
    status INTEGER DEFAULT 0 -- 0:Available, 1:Locked, 2:Booked, 3:Maintenance
);

-- 4. Bookings Table (The Transaction Record)
CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    slot_id INTEGER REFERENCES slots(slot_id), -- Foreign Key
    user_id INTEGER REFERENCES users(user_id),       -- Foreign Key
    payment_status VARCHAR(20) DEFAULT 'PENDING',
    payment_method VARCHAR(50),
    qr_token VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def init_db():
    try:
        print("Attempting to connect to the database")

        # get db url from .env
        DB_URL = os.getenv("DATABASE_URL")

        if not DB_URL:
            raise ValueError("No DATABASE_URL found! Check your .env file.")


        conn = pg2.connect(DB_URL)
        print("Connection successful")
        cur = conn.cursor()
        cur.execute(CREATE_TABLES_SQL)

        conn.commit()

        print("Tables created successfully")

        # clean up
        cur.close()
        conn.close()
        print("Connection closed")
    except Exception as e:
        print("An error occurred!")
        print(e)

if __name__ == "__main__":
    init_db()