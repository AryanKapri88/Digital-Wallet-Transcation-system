import uuid

# Class for a user
class User:
    def __init__(self, name, balance, tier):
        self.id = str(uuid.uuid4())  # Unique ID
        self.name = name
        self.balance = balance
        self.tier = tier  # Basic or Plus

    def get_limit(self):
        if self.tier == "basic":
            return 10000
        else:  # Plus
            return 20000

# Class to manage users
class UserManager:
    def __init__(self):
        self.users = {}  # Store users here

    def add_user(self, name, balance, tier="basic"):
        user = User(name, balance, tier)
        self.users[user.id] = user
        return user

    def get_user(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        print("❌ User not found!")
        return None