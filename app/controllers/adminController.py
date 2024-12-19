from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.adminSchema import AdminCreate, AdminUpdate, LoginSchema
from ..services.adminService import (
    retrieve_admin,
    get_admin,
    login,
    create_admin,
    update_admin,
    delete_admin,
    get_all_admins
)
from database import get_db

router = APIRouter()

# GET /admins - Retrieve all admins
@router.get("/read_all_admins")
def read_all_admins(db: Session = Depends(get_db)):
    admins = get_all_admins(db)
    if not admins:
        raise HTTPException(status_code=404, detail="No admins found")
    return admins

# GET /admin/{admin_id} - Retrieve a admin by ID
@router.get("/get/{admin_id}")
def read_admin_controller(admin_id: int, db: Session = Depends(get_db)):
    try:
        admin = get_admin(admin_id, db)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST /admin - Create a new admin
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_admin_controller(admin: AdminCreate, db: Session = Depends(get_db)):
    try:
        admin = create_admin(admin, db)
        return admin
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# PUT /admin/{admin_id} - Update a admin
@router.put("/updateAdmin/{admin_id}", status_code=status.HTTP_200_OK)
def update_admin_controller(admin_id: int, admin_update: AdminUpdate, db: Session = Depends(get_db)):
    try:
        admin = update_admin(admin_id, admin_update, db)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE /admin/{admin_id} - Delete a admin
@router.delete("/{admin_id}")
def delete_admin_controller(admin_id: int, db: Session = Depends(get_db)):
    try:
        admin = get_admin(admin_id, db)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        response = delete_admin(admin_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete admin")
        return {"message": "Admin deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST /login - Authenticate admin and generate token
@router.post("/login")
def get_admin_token(data: LoginSchema, db: Session = Depends(get_db)):
    try:
        token = login(data, db)
        return token
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
