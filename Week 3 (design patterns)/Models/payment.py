import random
import string
from Repository.database import Database

class Observer:
    def update(self, message):
        pass

class Subject:
    def register_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass

    def notify_observers(self, message):
        pass

class PaymentProcessor(Subject):
    def __init__(self, db: Database):
        self._transactions = []
        self._used_transaction_ids = set()
        self.db = db
        self._observers = []

    def _generate_transaction_id(self):
        characters = string.ascii_uppercase + string.digits
        while True:
            transaction_id = ''.join(random.choices(characters, k=6))
            if transaction_id not in self._used_transaction_ids:
                self._used_transaction_ids.add(transaction_id)
                return transaction_id

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

    def verify_pin(self, username):
        stored_pin = self.db.get_pin(username)
        if not stored_pin:
            print("PIN not set! Please contact support to set a PIN.")
            return False

        max_attempts = 3
        attempts = 0
        while attempts < max_attempts:
            entered_pin = input("Enter your PIN: ")
            if entered_pin == stored_pin:
                return True
            else:
                attempts += 1
                remaining_attempts = max_attempts - attempts
                if remaining_attempts > 0:
                    print(f"Incorrect PIN, please enter the correct PIN. {remaining_attempts} attempts remaining.")
                else:
                    print("Too many incorrect attempts! Transaction failed.")
                    self.notify_observers("Transaction failed: Too many incorrect PIN attempts.")
                    return False
        return False

    def process_transaction(self, user, transaction):
        if transaction is None:
            self.notify_observers("Transaction failed: No transaction provided.")
            return False, user

        can_proceed, updated_user = user.can_perform_transaction()
        if not can_proceed:
            self.notify_observers(f"Transaction failed: {updated_user.get_username()} cannot perform transaction.")
            return False, updated_user

        user = updated_user
        print(f"\nProcessing {transaction.get_transaction_type()}...")
        print(transaction.get_details())

        if not self.verify_pin(user.get_username()):
            self.notify_observers(f"Transaction failed: PIN verification failed for {user.get_username()}.")
            return False, user

        if user.deduct_balance(transaction.amount):
            transaction_id = self._generate_transaction_id()
            transaction_type = transaction.get_transaction_type()
            recipient = transaction.payee_name if transaction_type == "Money Transfer" else None
            transaction_mode = "P2P" if transaction_type == "Money Transfer" else "P2M"

            self._transactions.append({
                'transaction_id': transaction_id,
                'date': transaction.date,
                'type': transaction_type,
                'total_balance': user.balance + transaction.amount,
                'amount': transaction.amount,
                'remaining_balance': user.balance,
                'remarks': transaction.remarks,
                'user_id': user.get_username(),
                'recipient': recipient,
                'transaction_mode': transaction_mode
            })
            self.notify_observers(f"Transaction successful: {transaction_type} processed for {user.get_username()}.")
            return True, user
        else:
            self.notify_observers(f"Transaction failed: Insufficient balance for {user.get_username()}.")
            return False, user

    def get_transactions(self):
        return self._transactions