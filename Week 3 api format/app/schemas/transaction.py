from pydantic import BaseModel
from typing import Dict, Optional, Any
from datetime import datetime
from app.enums import TransactionType  # Import from enums

class TransactionCreate(BaseModel):
    type: TransactionType
    details: Dict[str, Any]

class Transaction(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    amount: float
    remarks: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}