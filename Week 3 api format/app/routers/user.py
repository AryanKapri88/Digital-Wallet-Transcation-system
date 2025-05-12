from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db
from app.enums import UserTier  # Import from enums
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating user: {user.name}, tier: {user.tier}")
        db_user = crud.create_user(db=db, user=user)
        logger.info(f"User created successfully: {db_user.id}")
        return db_user
    except ValueError as ve:
        logger.error(f"Validation error in create_user: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in create_user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@router.post("/{user_id}/upgrade-tier", response_model=schemas.User)
def upgrade_user_tier(user_id: int, tier_update: schemas.UserUpdateTier, db: Session = Depends(get_db)):
    try:
        logger.info(f"Upgrading user {user_id} to tier {tier_update.tier}")
        user = crud.update_user_tier(db, user_id, tier_update)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if tier_update.tier == UserTier.PREMIUM.value and user.budget < 1000.0:  # Compare as string
            raise HTTPException(status_code=400, detail="Insufficient budget for Premium tier")
        logger.info(f"User {user_id} upgraded successfully")
        return user
    except Exception as e:
        logger.error(f"Error in upgrade_user_tier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upgrade user tier: {str(e)}")