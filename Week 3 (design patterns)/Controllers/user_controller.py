from Models.user import BasicUser, PremiumUser
from Repository.database import Database


def create_user(username, initial_balance, choice, db: Database):
    user_class = BasicUser if choice == "1" else PremiumUser
    user = user_class(username, initial_balance, db)

    # Deduct subscription fee if Premium tier is selected
    if choice == "2" and initial_balance >= 1000:  # 1000 is the subscription fee
        subscription_fee = 1000
        user._balance -= subscription_fee
        print(f"Balance set to {user._balance} after deducting {subscription_fee} for {username}")
        print(f"Payment of {subscription_fee} successful! Setting up {username} as Premium User...")
        if db:
            db.update_user_balance(username, user._balance)
    elif choice == "2" and initial_balance < 1000:
        print("Insufficient balance for Premium subscription! Defaulting to Basic tier.")
        user = BasicUser(username, initial_balance, db)

    return user