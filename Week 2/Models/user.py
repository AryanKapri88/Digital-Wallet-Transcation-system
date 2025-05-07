from datetime import datetime, date
import sys
from Repository.database import Database

class User:
    def __init__(self, username, initial_balance, db: Database = None):
        self._username = username
        self._balance = 0
        self._transaction_count = 0
        self._last_transaction_date = None
        self.db = db
        self.set_balance(initial_balance)

    @property
    def balance(self):
        return self._balance

    def set_balance(self, amount):
        if amount >= 0:
            self._balance = amount
            print(f"Balance set to {self._balance} for {self._username}")
            if self.db:
                self.db.save_user(self._username, self._balance, self.__class__.__name__)
        else:
            print("Balance cannot be negative!")
            self._balance = 0
            if self.db:
                self.db.save_user(self._username, self._balance, self.__class__.__name__)

    def add_balance(self):
        try:
            amount = float(input("Enter amount to add to balance: "))
            if amount > 0:
                self._balance += amount
                print(f"Added {amount}. New balance: {self._balance}")
                if self.db:
                    self.db.update_user_balance(self._username, self._balance)
                return True
            else:
                print("Amount must be positive!")
                return False
        except ValueError:
            print("Invalid amount!")
            return False

    def deduct_balance(self, amount):
        if amount <= self._balance:
            self._balance -= amount
            self._increment_transaction_count()
            if self.db:
                self.db.update_user_balance(self._username, self._balance)
            return True
        else:
            print("Balance finished! Do you want to add balance?")
            print("1. Yes 2. No")
            choice = input("Enter choice (1 or 2): ")
            if choice == '1':
                if self.add_balance() and amount <= self._balance:
                    self._balance -= amount
                    self._increment_transaction_count()
                    if self.db:
                        self.db.update_user_balance(self._username, self._balance)
                    return True
            return self.handle_loan_option(amount)

    def handle_loan_option(self, amount):
        print("Do you want to take a loan from your associated bank?")
        print("1. Yes 2. No")
        loan_choice = input("Enter choice (1 or 2): ")
        if loan_choice == '1':
            try:
                loan_amount = float(input("Enter loan amount: "))
                if loan_amount <= 0:
                    print("Loan amount must be positive!")
                    return False
                interest_rate = 0.05  # 5% annual interest
                total_repayment = loan_amount * (1 + interest_rate)
                monthly_payment = total_repayment / 12
                print(f"You have taken {loan_amount} of loan for a year for 5% interest so you have to pay {monthly_payment:.2f} monthly.")
                self._balance += loan_amount
                print(f"Added {loan_amount}. New balance: {self._balance}")
                if self.db:
                    self.db.update_user_balance(self._username, self._balance)
                if amount <= self._balance:
                    self._balance -= amount
                    self._increment_transaction_count()
                    if self.db:
                        self.db.update_user_balance(self._username, self._balance)
                    return True
                else:
                    print("Transaction failed due to insufficient balance after loan.")
                    sys.exit()
            except ValueError:
                print("Invalid loan amount!")
                return False
        else:
            print("Transaction failed due to insufficient balance.")
            sys.exit()

    def _increment_transaction_count(self):
        current_date = date.today()
        if self._last_transaction_date != current_date:
            self._transaction_count = 0
            self._last_transaction_date = current_date
        self._transaction_count += 1

    def can_perform_transaction(self):
        return True, self

    def upgrade_to_premium(self):
        pass

    def get_username(self):
        return self._username

class BasicUser(User):
    MAX_TRANSACTIONS_PER_DAY = 5

    def can_perform_transaction(self):
        current_date = date.today()
        if self._last_transaction_date != current_date:
            self._transaction_count = 0
            self._last_transaction_date = current_date
        if self._transaction_count >= self.MAX_TRANSACTIONS_PER_DAY:
            print("Transactions for the day exceeded. Do you want to upgrade to Premium?")
            print("1. Yes 2. No")
            choice = input("Enter choice (1 or 2): ")
            if choice == '1':
                new_user, success = self.upgrade_to_premium()
                if success:
                    return True, new_user
                return False, self
            else:
                print("Transaction exceeded, try tomorrow.")
                return False, self
        return True, self

    def upgrade_to_premium(self):
        subscription_fee = 1000
        print(f"Premium subscription requires a payment of {subscription_fee} for a whole year.")
        if self._balance >= subscription_fee:
            self._balance -= subscription_fee
            print(f"Balance set to {self._balance} after deducting {subscription_fee} for {self._username}")
            print(f"Payment of {subscription_fee} successful! Upgrading {self._username} to Premium User...")
            if self.db:
                self.db.update_user_balance(self._username, self._balance)
            user = PremiumUser(self._username, self._balance, self.db)
            user._transaction_count = self._transaction_count
            user._last_transaction_date = self._last_transaction_date
            return user, True
        else:
            print("Insufficient balance for Premium subscription! Please add funds.")
            if self.add_balance() and self._balance >= subscription_fee:
                self._balance -= subscription_fee
                print(f"Balance set to {self._balance} after deducting {subscription_fee} for {self._username}")
                print(f"Payment of {subscription_fee} successful! Upgrading {self._username} to Premium User...")
                if self.db:
                    self.db.update_user_balance(self._username, self._balance)
                user = PremiumUser(self._username, self._balance, self.db)
                user._transaction_count = self._transaction_count
                user._last_transaction_date = self._last_transaction_date
                return user, True
            print("Upgrade failed due to insufficient balance.")
            return self, False

class PremiumUser(User):
    def can_perform_transaction(self):
        return True, self

    def get_username(self):
        return self._username