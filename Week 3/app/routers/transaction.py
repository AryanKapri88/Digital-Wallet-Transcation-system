from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.enums import TransactionType, UserTier
from datetime import date

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify transaction type
    if transaction.type not in [TransactionType.MONEY_TRANSFER, TransactionType.BILL_PAYMENT, TransactionType.MOBILE_RECHARGE]:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    # Check daily transaction limit for Basic tier
    if user.tier == UserTier.BASIC.value:
        today_count = crud.get_transaction_count_today(db, user.id)
        if today_count >= 5:
            raise HTTPException(status_code=400, detail="Daily transaction limit reached for Basic tier")

    # Refresh user to get the latest budget
    db.refresh(user)

    # Check budget with the latest value
    amount = transaction.details.get("amount", 0.0)
    if user.budget < amount:
        raise HTTPException(status_code=400, detail="Insufficient budget")

    # Update user budget within the session
    user.budget -= amount
    db.commit()

    # Create transaction
    return crud.create_transaction(
        db=db,
        user_id=user.id,
        transaction_data=transaction.details,
        amount=amount,
        type=transaction.type,
        remarks=transaction.details.get("remarks")
    )

@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transactions = crud.get_transactions_by_user(db, user_id=user.id, skip=skip, limit=limit)
    return transactions