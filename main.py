from fastapi import FastAPI, Depends, HTTPException
from utils.database import get_db_connection
from pydantic import BaseModel
from enum import Enum

class SlotStatus(Enum):
    AVAILABLE = 0
    BOOKED = 2

class BookingRequest(BaseModel):
    slot_id: int
    user_id: int

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

@app.post("/book")
def book_stall( request: BookingRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT status FROM availability WHERE slot_id = %s FOR UPDATE;", 
            (request.slot_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Slot not found")
        
        current_status = row['status']

        if current_status != SlotStatus.AVAILABLE.value:
            conn.rollback() # Cancel transaction
            # Return 409 Conflict (standard for "state conflict")
            raise HTTPException(status_code=409, detail="Too slow! This slot is already booked.")
        
        cursor.execute(
            "UPDATE availability SET status = %s WHERE slot_id = %s;",
            (SlotStatus.BOOKED.value, request.slot_id)
        )
        cursor.execute(
            """
            INSERT INTO bookings (slot_id, user_id, payment_status) 
            VALUES (%s, %s, 'PENDING') 
            RETURNING booking_id;
            """,
            (request.slot_id, request.user_id)
        )
        new_booking_id = cursor.fetchone()['booking_id']

        conn.commit() # Commit transaction
        
        return {
            "status": "success", 
            "message": "Booking confirmed!", 
            "booking_id": new_booking_id
        }
    except Exception as e:
        conn.rollback() # If any error happens, undo everything
        # If it's already an HTTPException (like 409 or 404), re-raise it
        if isinstance(e, HTTPException):
            raise e
        # Otherwise, it's a server error
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()

@app.get("/availability")
def get_availability( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()

        query = """
        SELECT 
            a.slot_id, 
            a.date,
            a.price
        FROM availability a
        JOIN stalls s ON a.stall_id = s.stall_id
        WHERE a.status = 0;
        """
        cursor.execute(query)
        slots = cursor.fetchall()
        cursor.close()
        return slots
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching availability: {e}")