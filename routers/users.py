from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.database import get_db_connection

router = APIRouter()

@router.get("/get_users")
def get_users( conn = Depends(get_db_connection) ):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        cursor.close()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")
    
class CreateUserRequest(BaseModel):
    line_uid: str
    name: str
@router.post("/create_user")
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
@router.post("/delete_user")
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