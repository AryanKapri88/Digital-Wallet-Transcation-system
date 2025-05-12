import enum

class TransactionType(str, enum.Enum):
    MONEY_TRANSFER = "money_transfer"
    BILL_PAYMENT = "bill_payment"
    MOBILE_RECHARGE = "mobile_recharge"

class UserTier(str, enum.Enum):
    BASIC = "basic"
    PREMIUM = "premium"