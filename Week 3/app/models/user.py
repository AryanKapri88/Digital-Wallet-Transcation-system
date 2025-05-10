from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    pin = Column(String, nullable=False)  # Store PIN as string (hashed in production)
    budget = Column(Float, default=0.0, nullable=False)
    tier = Column(String, default="basic", nullable=False)  # Changed to String

    # Add the transactions relationship
    transactions = relationship("Transaction", back_populates="user")