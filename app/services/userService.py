from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..models.user import User
from ..schemas.userSchema import UserCreate, UserUpdate, LoginSchema
from database import get_db
from ..services.utils import verify_password, create_access_token, get_hashed_password
import logging


def retrieve_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()


def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return user


def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    token = create_access_token(user.id)
    return {"token": token, "id": user.id}


def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=422, detail="Cet email est déjà utilisé.")
    
    hashed_password = get_hashed_password(user.password)
    
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        firstname=user.firstname,
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        logging.error(f"Erreur lors de la création de l'utilisateur : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur avec l'ID {user_id} non trouvé")
    
    user.name = user_update.name if user_update.name else user.name
    user.firstname = user_update.firstname if user_update.firstname else user.firstname
    user.password = get_hashed_password(user_update.password) if user_update.password else user.password
    user.email = user_update.email if user_update.email else user.email
    
    db.commit()
    db.refresh(user)
    return user


def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur avec l'ID {user_id} non trouvé")
    db.delete(user)
    db.commit()
    return True


def get_all_users(db: Session = Depends(get_db)):
    try:
        logging.info("Récupération de tous les utilisateurs de la base de données")
        users = db.query(User).all()
        logging.info(f"{len(users)} utilisateurs récupérés")
        return users
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des utilisateurs : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
