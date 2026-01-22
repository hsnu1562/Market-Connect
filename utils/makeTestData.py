import os
import psycopg2 as pg2
from dotenv import load_dotenv   


load_dotenv()
conn = pg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

print("Inserting test stall...")
cur.execute("""
    INSERT INTO stalls (location_name, lat, long, facilities, owner_id)
    VALUES ('Taipei Night Market - Entrance A', 25.0330, 121.5654, 'Water, Electricity', 1);
""")
conn.commit()
print("Done!")
conn.close()