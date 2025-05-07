from Models.user import BasicUser, PremiumUser
from Repository.database import Database


def create_user(username, initial_balance, choice, db: Database):
    user_class = BasicUser if choice == "1" else PremiumUser
    user = user_class(username, initial_balance, db)
    return user