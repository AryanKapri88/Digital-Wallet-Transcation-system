from pydantic import BaseModel, field_validator
from app.enums import UserTier  # Import from enums

class UserBase(BaseModel):
    name: str
    pin: str
    budget: float

class UserCreate(UserBase):
    tier: UserTier = UserTier.BASIC

    @field_validator("tier", mode="before")
    def validate_tier(cls, value):
        if not isinstance(value, str):
            raise ValueError("tier must be a string")
        value = value.lower()
        if value not in ["basic", "premium"]:
            raise ValueError("tier must be 'basic' or 'premium'")
        return value

class UserUpdateTier(BaseModel):
    tier: UserTier

    @field_validator("tier", mode="before")
    def validate_tier(cls, value):
        if not isinstance(value, str):
            raise ValueError("tier must be a string")
        value = value.lower()
        if value not in ["basic", "premium"]:
            raise ValueError("tier must be 'basic' or 'premium'")
        return value

class User(UserBase):
    id: int
    tier: UserTier

    model_config = {"from_attributes": True}