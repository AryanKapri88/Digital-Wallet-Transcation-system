import uuid
from datetime import datetime

# Class to handle payments
class PaymentGateway:
    def __init__(self):
        self.payments = []  # List to store payments

    def pay(self, user, amount):
        if amount <= 0:
            print("❌ Payment must be more than 0!")
            return
        if amount > user.balance:
            print("❌ Not enough money!")
            return
        user.balance -= amount
        payment = {
            "id": str(uuid.uuid4()),
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.payments.append(payment)
        print(f"💳 Paid {amount}!")