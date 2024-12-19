from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..models.admin import Admin
from ..schemas.adminSchema import AdminCreate, AdminUpdate, LoginSchema
from database import get_db
from ..services.utils import verify_password, create_access_token, get_hashed_password
import logging


def retrieve_admin(admin_id: int, db: Session = Depends(get_db)):
    return db.query(Admin).filter(Admin.id == admin_id).first()


def get_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return admin


def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == login_data.email).first()
    
    if not admin or not verify_password(login_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    token = create_access_token(admin.id)
    return {"token": token, "id": admin.id}


def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    if db.query(Admin).filter(Admin.email == admin.email).first():
        raise HTTPException(status_code=422, detail="Cet email est déjà utilisé.")
    
    hashed_password = get_hashed_password(admin.password)
    
    db_admin = Admin(
        name=admin.name,
        email=admin.email,
        password=hashed_password,
        
    )
    
    try:
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        return db_admin
    except Exception as e:
        logging.error(f"Erreur lors de la création de l'utilisateur : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


def update_admin(admin_id: int, admin_update: AdminUpdate, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    
    if not admin:
        raise HTTPException(status_code=404, detail=f"Utilisateur avec l'ID {admin_id} non trouvé")
    
    admin.name = admin_update.name if admin_update.name else admin.name
    admin.password = get_hashed_password(admin_update.password) if admin_update.password else admin.password
    admin.email = admin_update.email if admin_update.email else admin.email
    
    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = get_admin(admin_id, db)
    if not admin:
        raise HTTPException(status_code=404, detail=f"Utilisateur avec l'ID {admin_id} non trouvé")
    db.delete(admin)
    db.commit()
    return True


def get_all_admins(db: Session = Depends(get_db)):
    try:
        logging.info("Récupération de tous les utilisateurs de la base de données")
        admins = db.query(Admin).all()
        logging.info(f"{len(admins)} utilisateurs récupérés")
        return admins
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des utilisateurs : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
