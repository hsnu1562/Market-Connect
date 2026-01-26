from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.database import get_db_connection

router = APIRouter()

@router.get("/get_availability")
def get_availability( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM availability;")
        availability = cursor.fetchall()
        cursor.close()
        return availability
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching availability: {e}")

class CreateAvailabilityRequest(BaseModel):
    stall_id: int
    date: str
    price: int
@router.post("/create_availability")
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
@router.post("/delete_availability")
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