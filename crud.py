from sqlalchemy.orm import Session
#from . 
import models, schemas

def get_user(db: Session, userID: int):
    return db.query(models.User).filter(models.User.id == userID).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    dbUser = models.User(username=user.username, email=user.email, password=user.password, isLogged=False)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser

def update_user(db:Session, userID: int, data: dict):
    dbUser = db.query(models.User).filter(models.User.id == userID).first()
    for key in data.keys():
        setattr(dbUser, key, data[key])
    db.commit()
    db.refresh(dbUser)
    return dbUser

def delete_user(db: Session, userID: int):
    dbUser = db.query(models.User).filter(models.User.id == userID).first()
    db.delete(dbUser)
    db.commit()
    return dbUser

def login(db: Session, username: str):
    dbUser = db.query(models.User).filter(models.User.username == username).first()
    dbUser.isLogged = True
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)

def logout(db: Session, username: str):
    try:
        dbUser = db.query(models.User).filter(models.User.username == username).first()
        dbUser.isLogged = False
        db.add(dbUser)
        db.commit()
        db.refresh(dbUser)
        return True
    except:
        return False