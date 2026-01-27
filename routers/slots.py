from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.database import get_db_connection

router = APIRouter()

@router.get("/get_slots")
def get_slots( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM slots;")
        slots = cursor.fetchall()
        cursor.close()
        return slots
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching slots: {e}")

class CreateSlotsRequest(BaseModel):
    stall_id: int
    date: str
    price: int
@router.post("/create_slot")
def create_slot( request: CreateSlotsRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO slots (stall_id, date, price, status) 
            VALUES (%s, %s, %s, 0) 
            RETURNING slot_id;
            """,
            (request.stall_id, request.date, request.price)
        )
        new_slot_id = cursor.fetchone()['slot_id']
        conn.commit()
        return {
            "status": "success",
            "message": "slot created successfully!",
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

class DeleteSlotsRequest(BaseModel):
    slot_id: int
@router.post("/delete_slot")
def delete_slot( request: DeleteSlotsRequest, conn = Depends(get_db_connection) ):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM slots WHERE slot_id = %s;",
            (request.slot_id,)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Slot not found")
        
        conn.commit()
        return {
            "status": "success",
            "message": "Slot deleted successfully!"
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