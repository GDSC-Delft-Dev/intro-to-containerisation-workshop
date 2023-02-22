"""
REST API endpoints.
"""
import os
import uvicorn
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
from schemas import User, UserCreate, UserPatch, UserUpdate, UserPatchPassword, UserLogin
from models import Base
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intro to Containerisation REST API 🐳📦🚢",
    description="This is a REST API used for 'Introduction to Containerisation Workshop' by GDSC",
    version="1.0.0",
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def get_hello_world():
    """Get a hello world response.
    """
    return "Hello World!"


@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/login/")
def log_in_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Login Failed!")

    hashed_password = crud.hash_password(user.password)
    
    logged_in = db_user.hashed_password == hashed_password
    if not logged_in:
        raise HTTPException(status_code=400, detail="Login Failed!")
    return {"success" : logged_in}

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserPatch, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    return crud.update_user(db=db, db_user=db_user)

@app.patch("/users/password/{user_id}", response_model=User)
def update_user_password(user_id: int, user: UserPatchPassword, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.hashed_password = crud.hash_password(user.password)

    return crud.update_user(db=db, db_user=db_user)

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user).items():
        setattr(db_user, var, value)

    db_user.hashed_password = crud.hash_password(user.password)

    return crud.update_user(db=db, db_user=db_user)

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.delete_user(db=db, db_user=db_user)



if __name__=="__main__":
    uvicorn.run(
        app,
        host=os.getenv("ADDRESS", "localhost"),
        port=5000,
        reload=False
    )
