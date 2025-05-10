from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database import SessionLocal
from app.models.user import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(pin: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.pin == pin).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid PIN")
    return user