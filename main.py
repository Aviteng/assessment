from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

#from . 
import crud, models, schemas
# from .
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    dbUser = crud.get_user_by_email(db, email=user.email)
    if dbUser:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{userID}", response_model=schemas.User)
def get_user(userID: int, db: Session = Depends(get_db)):
    dbUser = crud.get_user(db, userID=userID)
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dbUser

@app.put("/users/{userID}", response_model=schemas.User)
def updateUser(userID: int, data: dict, db: Session = Depends(get_db)):
    dbUser = crud.update_user(db, userID, data)
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dbUser

@app.delete("/users/{userID}", response_model=schemas.User)
def deleteUser(userID: int, db: Session = Depends(get_db)):
    dbUser = crud.delete_user(db, userID)
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dbUser

@app.post("/login", response_model=schemas.User)
async def loginUser(request: Request, db: Session = Depends(get_db)):
    req = await request.json()
    username = req['username']
    password = req['password']
    dbUser = crud.get_user_by_username(db, username)
    if dbUser.password != password :
        raise HTTPException(status_code=404, detail="Password not correct")
    crud.login(db, username)
    return dbUser

@app.post("/logout")
async def loginUser(request: Request, db: Session = Depends(get_db)):
    req = await request.json()
    username = req['username']
    return crud.logout(db, username)