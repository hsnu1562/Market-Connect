from fastapi import FastAPI, Depends, HTTPException
from utils.database import get_db_connection
from pydantic import BaseModel
from enum import Enum

class SlotStatus(Enum):
    AVAILABLE = 0
    LOCKED = 1
    BOOKED = 2

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


@app.get("/get_users")
def get_users( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        cursor.close()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")

@app.get("/get_stalls")
def get_stalls( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stalls;")
        stalls = cursor.fetchall()
        cursor.close()
        return stalls
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stalls: {e}")

@app.get("/get_availability")
def get_availability( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM availability;")
        availability = cursor.fetchall()
        cursor.close()
        return availability
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching availability: {e}")

@app.get("/get_bookings")
def get_bookings( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings;")
        bookings = cursor.fetchall()
        cursor.close()
        return bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bookings: {e}")

class BookingRequest(BaseModel):
    slot_id: int
    user_id: int
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

@app.get("/available_slots")
def get_available_slots( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()

        query = """
        SELECT 
            a.slot_id, 
            a.date,
            a.price,
            a.status
        FROM availability a
        JOIN stalls s ON a.stall_id = s.stall_id
        WHERE a.status = 0;
        """
        cursor.execute(query)
        slots = cursor.fetchall()
        cursor.close()
        return slots
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching available slots: {e}")

class CreateUserRequest(BaseModel):
    line_uid: str
    name: str
@app.post("/create_user")
def create_user( user: CreateUserRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (line_uid, name) 
            VALUES (%s, %s) 
            RETURNING user_id;
            """,
            (user.line_uid, user.name)
        )
        new_user_id = cursor.fetchone()['user_id']
        conn.commit()
        return {
            "status": "success",
            "message": "User created successfully!",
            "user_id": new_user_id,
            "user_name": user.name
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

class DeleteUserRequest(BaseModel):
    user_id: int
@app.post("/delete_user")
def delete_user( request: DeleteUserRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM users WHERE user_id = %s;",
            (request.user_id,)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="User not found")
        
        conn.commit()
        return {
            "status": "success",
            "message": "User deleted successfully!"
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

class CreateStallRequest(BaseModel):
    location_name: str
    facilities: str
@app.post("/create_stall")
def create_stall( request: CreateStallRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO stalls (location_name, facilities) 
            VALUES (%s, %s) 
            RETURNING stall_id;
            """,
            (request.location_name, request.facilities)
        )
        new_stall_id = cursor.fetchone()['stall_id']
        conn.commit()
        return {
            "status": "success",
            "message": "Stall created successfully!",
            "stall_id": new_stall_id,
            "location_name": request.location_name,
            "facilities": request.facilities
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

class DeleteStallRequest(BaseModel):
    stall_id: int
@app.post("/delete_stall")
def delete_stall( request: DeleteStallRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM stalls WHERE stall_id = %s;",
            (request.stall_id,)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Stall not found")
        
        conn.commit()
        return {
            "status": "success",
            "message": "Stall deleted successfully!"
        }
    except Exception as e:
        conn.rollback()
        # If it's already an HTTPException (like 409 or 404), re-raise it
        if isinstance(e, HTTPException):
            raise e
        # Otherwise, it's a server error
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()

class CreateAvailabilityRequest(BaseModel):
    stall_id: int
    date: str
    price: int
@app.post("/create_availability")
def create_availability( request: CreateAvailabilityRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO availability (stall_id, date, price, status) 
            VALUES (%s, %s, %s, 0) 
            RETURNING slot_id;
            """,
            (request.stall_id, request.date, request.price)
        )
        new_slot_id = cursor.fetchone()['slot_id']
        conn.commit()
        return {
            "status": "success",
            "message": "Availability slot created successfully!",
            "slot_id": new_slot_id,
            "stall_id": request.stall_id,
            "date": request.date,
            "price": request.price
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

class DeleteAvailabilityRequest(BaseModel):
    slot_id: int
@app.post("/delete_availability")
def delete_availability( request: DeleteAvailabilityRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM availability WHERE slot_id = %s;",
            (request.slot_id,)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Availability slot not found")
        
        conn.commit()
        return {
            "status": "success",
            "message": "Availability slot deleted successfully!"
        }
    except Exception as e:
        conn.rollback()
        # If it's already an HTTPException (like 409 or 404), re-raise it
        if isinstance(e, HTTPException):
            raise e
        # Otherwise, it's a server error
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()

@app.post("/delete_booking")
def delete_booking( request: DeleteAvailabilityRequest, conn = Depends(get_db_connection) ):
    # note: this only deletes the booking record, does not free up the slot
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM bookings WHERE booking_id = %s;",
            (request.slot_id,)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Booking not found")
        
        conn.commit()
        return {
            "status": "success",
            "message": "Booking deleted successfully!"
        }
    except Exception as e:
        conn.rollback()
        # If it's already an HTTPException (like 409 or 404), re-raise it
        if isinstance(e, HTTPException):
            raise e
        # Otherwise, it's a server error
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()