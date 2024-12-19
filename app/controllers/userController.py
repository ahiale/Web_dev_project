from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.userSchema import UserCreate, UserUpdate, LoginSchema
from ..services.userService import (
    retrieve_user,
    get_user,
    login,
    create_user,
    update_user,
    delete_user,
    get_all_users
)
from database import get_db

router = APIRouter()

# GET /users - Retrieve all users
@router.get("/read_all_users")
def read_all_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# GET /user/{user_id} - Retrieve a user by ID
@router.get("/get/{user_id}")
def read_user_controller(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_user(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST /user - Create a new user
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user_controller(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(user, db)
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# PUT /user/{user_id} - Update a user
@router.put("/updateUser/{user_id}", status_code=status.HTTP_200_OK)
def update_user_controller(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = update_user(user_id, user_update, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE /user/{user_id} - Delete a user
@router.delete("/{user_id}")
def delete_user_controller(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_user(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        response = delete_user(user_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete user")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST /login - Authenticate user and generate token
@router.post("/login")
def get_user_token(data: LoginSchema, db: Session = Depends(get_db)):
    try:
        token = login(data, db)
        return token
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
