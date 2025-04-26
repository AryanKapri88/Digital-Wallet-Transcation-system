import random
import string
from user_tier import BasicUser, PremiumUser

class PaymentProcessor:
    def __init__(self):
        self._pin = self._set_pin()
        self._transactions = []
        self._used_transaction_ids = set()

    def _set_pin(self):
        pin = input("Set your 4-digit PIN: ")
        while not (pin.isdigit() and len(pin) == 4):
            print("PIN must be a 4-digit number!")
            pin = input("Set your 4-digit PIN: ")
        return pin

    def _generate_transaction_id(self):
        characters = string.ascii_uppercase + string.digits
        while True:
            transaction_id = ''.join(random.choices(characters, k=6))
            if transaction_id not in self._used_transaction_ids:
                self._used_transaction_ids.add(transaction_id)
                return transaction_id

    def verify_pin(self):
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            entered_pin = input("Enter your PIN: ")
            if entered_pin == self._pin:
                return True
            else:
                attempts += 1
                remaining_attempts = max_attempts - attempts
                if remaining_attempts > 0:
                    print(f"Incorrect PIN, please enter the correct PIN. {remaining_attempts} attempts remaining.")
                else:
                    print("Too many incorrect attempts! Transaction failed.")
                    return False
        return False

    def process_transaction(self, user, transaction):
        if transaction is None:
            return False, user

        can_proceed, updated_user = user.can_perform_transaction()
        if not can_proceed:
            return False, updated_user

        user = updated_user  # Update user to reflect any upgrades

        print(f"\nProcessing {transaction.get_transaction_type()}...")
        print(transaction.get_details())

        if not self.verify_pin():
            return False, user

        if user.deduct_balance(transaction.amount):
            transaction_id = self._generate_transaction_id()
            self._transactions.append({
                'transaction_id': transaction_id,
                'date': transaction.date,
                'type': transaction.get_transaction_type(),
                'total_balance': user.balance + transaction.amount,
                'amount': transaction.amount,
                'remaining_balance': user.balance,
                'remarks': transaction.remarks
            })
            print(f"Transaction successful! Transaction ID: {transaction_id}")
            return True, user
        else:
            return False, user

    def get_transactions(self):
        return self._transactions