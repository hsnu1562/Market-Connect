from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.database import get_db_connection

router = APIRouter()

@router.get("/get_bookings")
def get_bookings( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings;")
        bookings = cursor.fetchall()
        cursor.close()
        return bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bookings: {e}")

class DeleteBookingRequest(BaseModel):
    booking_id: int
@router.post("/delete_booking")
def delete_booking( request: DeleteBookingRequest, conn = Depends(get_db_connection) ):
    # note: this only deletes the booking record, does not free up the slot
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM bookings WHERE booking_id = %s;",
            (request.booking_id,)
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