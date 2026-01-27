from fastapi import APIRouter, Depends, HTTPException
from utils.database import get_db_connection

router = APIRouter()

@router.get("/get_available_slots")
def get_available_slots( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()

        query = """
        SELECT 
            a.slot_id, 
            a.date,
            a.price,
            a.status
        FROM slots a
        JOIN stalls s ON a.stall_id = s.stall_id
        WHERE a.status = 0;
        """
        cursor.execute(query)
        slots = cursor.fetchall()
        cursor.close()
        return slots
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching available slots: {e}")