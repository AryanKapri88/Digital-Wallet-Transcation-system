from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionType
from datetime import datetime, date

def create_transaction(
    db: Session,
    user_id: int,
    transaction_data: dict,
    amount: float,
    type: TransactionType,
    remarks: str | None = None
):
    db_transaction = Transaction(
        user_id=user_id,
        type=type,
        amount=amount,
        remarks=remarks,
        created_at=datetime.utcnow()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all())

def get_transaction_count_today(db: Session, user_id: int):
    today = date.today()
    return (db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .filter(Transaction.created_at >= datetime.combine(today, datetime.min.time()))
            .count())