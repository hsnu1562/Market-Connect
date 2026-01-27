from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.database import get_db_connection
from routers.enums import SlotStatus

router = APIRouter()

class BookingRequest(BaseModel):
    user_id: int
    slot_id: int
@router.post("/book")
def book_stall( request: BookingRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT status FROM slots WHERE slot_id = %s FOR UPDATE;", 
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
            "UPDATE slots SET status = %s WHERE slot_id = %s;",
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
