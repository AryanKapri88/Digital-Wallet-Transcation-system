from datetime import datetime
import pandas as pd
import uuid

# Class for a transaction
class Transaction:
    def __init__(self, amount, category, type):
        self.id = str(uuid.uuid4())  # Unique ID
        self.amount = amount
        self.category = category.lower()
        self.type = type  # Transfer or Load
        self.date = datetime.now().strftime("%Y-%m-%d")

    def get_info(self):
        return {"id": self.id, "date": self.date, "category": self.category, "amount": self.amount, "type": self.type}

# Class to manage transactions
class TransactionManager:
    def __init__(self):
        self.transactions = []  # List to store transactions

    def add_category(self, category):
        print(f"✅ Noted category '{category}'! You can use any category name.")

    def transfer(self, sender, receiver, amount, category):
        if amount <= 0:
            print("❌ Amount must be more than 0!")
            return
        if amount > sender.balance:
            print("❌ Not enough money!")
            return
        if amount > sender.get_limit():
            print("❌ Too much for your tier!")
            return
        if not receiver:
            print("❌ Must pick a receiver!")
            return
        sender.balance -= amount
        receiver.balance += amount
        transaction = Transaction(amount, category, "transfer")
        self.transactions.append(transaction.get_info())
        print(f"🎉 Transferred {amount} to {receiver.name}!")

    def load_wallet(self, user, amount, category):
        if amount <= 0:
            print("❌ Amount must be more than 0!")
            return
        user.balance += amount
        transaction = Transaction(amount, category, "load")
        self.transactions.append(transaction.get_info())
        print(f"🎉 Added {amount} to your wallet!")

    def save(self, balance):
        if not self.transactions:
            print("❌ Nothing to save!")
            return
        df = pd.DataFrame(self.transactions)
        with open("wallet.csv", "w") as f:
            f.write(f"Balance,{balance}\n")
            df.to_csv(f, index=False)
        print("✅ Saved to wallet.csv!")