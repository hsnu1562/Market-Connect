from fastapi import FastAPI, Depends, HTTPException
from utils.database import get_db_connection

# Initialize the app
app = FastAPI(
    title="Market Connect API",
    description="Backend API for stall reservation system",
    version="0.0.0"
)

# When someone visits homepage, say hello
@app.get("/")
def read_root():
    return {"message": "Welcome to the Market Connect API! System is online"}

@app.get("/test_stalls")
def get_fake_stalls():
    return [
        {"id": 1, "name": "Taipei Main Station Exit M3", "status": "Available"},
        {"id": 2, "name": "Zhongshan Park Entrance", "status": "Booked"}        
    ]

@app.get("/stalls")
def get_stalls( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stalls;")
        stalls = cursor.fetchall()
        cursor.close()
        return stalls
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stalls: {e}")