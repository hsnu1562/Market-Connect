# /book: Endpoint to book a stall slot

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
    """
    books a stall by user_id and slot_id
    """
    cursor = conn.cursor()
    try:
        # Check if user exists
        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = %s;", 
            (request.user_id,)
        )
        user_row = cursor.fetchone()
        if not user_row:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if slot exists and is available
        cursor.execute(
            "SELECT status FROM slots WHERE slot_id = %s FOR UPDATE;", 
            (request.slot_id,)
        )
        slot_row = cursor.fetchone()
        if not slot_row:
            raise HTTPException(status_code=404, detail="Slot not found")
        
        current_status = slot_row['status']

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
            INSERT INTO bookings (user_id, slot_id, payment_status) 
            VALUES (%s, %s, 'PENDING') 
            RETURNING booking_id;
            """,
            (request.user_id, request.slot_id)
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
