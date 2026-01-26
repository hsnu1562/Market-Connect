from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.database import get_db_connection

router = APIRouter()

@router.get("/get_stalls")
def get_stalls( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stalls;")
        stalls = cursor.fetchall()
        cursor.close()
        return stalls
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stalls: {e}")
    
class CreateStallRequest(BaseModel):
    location_name: str
    facilities: str
@router.post("/create_stall")
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
@router.post("/delete_stall")
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