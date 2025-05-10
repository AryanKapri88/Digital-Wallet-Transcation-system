from sqlalchemy.orm import Session
from app import schemas
from app.models.user import User
from app.enums import UserTier
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Valid tier values
VALID_TIERS = {UserTier.BASIC.value, UserTier.PREMIUM.value}


def create_user(db: Session, user: schemas.UserCreate):
    try:
        logger.info(f"Starting user creation/update for name: {user.name}")

        # Check if a user with the same name already exists
        existing_user = db.query(User).filter(User.name == user.name).first()

        if existing_user:
            # Update existing user's details
            logger.info(f"User with name {user.name} already exists, updating details")
            existing_user.pin = user.pin
            existing_user.budget = user.budget
            existing_user.tier = user.tier

            # Validate tier for the updated user
            if existing_user.tier not in VALID_TIERS:
                raise ValueError(f"Invalid tier: {existing_user.tier}. Must be one of {VALID_TIERS}")

            # Adjust budget based on tier
            adjusted_budget = existing_user.budget
            if existing_user.tier == UserTier.PREMIUM.value:
                adjusted_budget -= 1000.0  # Deduct premium fee
                if adjusted_budget < 0:
                    raise ValueError("Insufficient budget for premium tier")
            existing_user.budget = adjusted_budget
            logger.info(f"Adjusted budget: {adjusted_budget:.2f}")

            # Commit the updates
            db.commit()
            logger.info("Database commit successful for update")

            # Refresh the user object
            db.refresh(existing_user)
            logger.info(f"User updated and refreshed from database: {existing_user.id}")

            return existing_user

        # If no existing user, create a new one
        logger.info(f"No existing user with name {user.name}, creating new user")

        # Validate tier
        if user.tier not in VALID_TIERS:
            raise ValueError(f"Invalid tier: {user.tier}. Must be one of {VALID_TIERS}")

        # Adjust budget based on tier
        adjusted_budget = user.budget
        if user.tier == UserTier.PREMIUM.value:
            adjusted_budget -= 1000.0  # Deduct premium fee
            if adjusted_budget < 0:
                raise ValueError("Insufficient budget for premium tier")
        logger.info(f"Adjusted budget: {adjusted_budget:.2f}")

        # Create user object
        db_user = User(
            name=user.name,
            pin=user.pin,
            budget=adjusted_budget,
            tier=user.tier
        )
        logger.info(f"User object created: {db_user.name}")

        # Add to session and commit
        db.add(db_user)
        logger.info("User added to session")
        db.commit()
        logger.info("Database commit successful")

        # Refresh the user object to get the updated ID
        db.refresh(db_user)
        logger.info(f"User refreshed from database: {db_user.id}")

        return db_user
    except Exception as e:
        logger.error(f"Error creating/updating user: {str(e)}")
        raise


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user_tier(db: Session, user_id: int, tier_update: schemas.UserUpdateTier):
    user = get_user(db, user_id)
    if not user:
        return None

    # Validate tier
    if tier_update.tier not in VALID_TIERS:
        raise ValueError(f"Invalid tier: {tier_update.tier}. Must be one of {VALID_TIERS}")

    user.tier = tier_update.tier
    db.commit()
    db.refresh(user)
    return user