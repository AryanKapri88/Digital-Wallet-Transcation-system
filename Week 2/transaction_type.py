from datetime import datetime

class Transaction:
    def __init__(self, amount, remarks):
        self.amount = amount
        self.remarks = remarks
        self.date = datetime.now()

    def get_details(self):
        return f"Transaction - Amount: {self.amount}, Remarks: {self.remarks}"

    def get_transaction_type(self):
        return "Generic Transaction"

class MoneyTransfer(Transaction):
    def __init__(self, payee_name, bank, amount, remarks):
        super().__init__(amount, remarks)
        self.payee_name = payee_name
        self.bank = bank

    def get_details(self):
        return f"Money Transfer to {self.payee_name} ({self.bank}) - Amount: {self.amount}, Remarks: {self.remarks}"

    def get_transaction_type(self):
        return "Money Transfer"

class BillPayment(Transaction):
    def __init__(self, bill_category, amount, remarks):
        super().__init__(amount, remarks)
        self.bill_category = bill_category

    def get_details(self):
        return f"Bill Payment ({self.bill_category}) - Amount: {self.amount}, Remarks: {self.remarks}"

    def get_transaction_type(self):
        return "Bill Payment"

class MobileRecharge(Transaction):
    def __init__(self, mobile_number, amount, remarks):
        super().__init__(amount, remarks)
        self.mobile_number = mobile_number

    def get_details(self):
        return f"Mobile Recharge ({self.mobile_number}) - Amount: {self.amount}, Remarks: {self.remarks}"

    def get_transaction_type(self):
        return "Mobile Recharge"

def perform_transaction(user):
    print("\nChoose transaction type: 1. Money Transfer 2. Bill Payment 3. Mobile Recharge")
    choice = input("Enter choice (1, 2, or 3): ")

    if choice == '1':
        payee_name = input("Enter payee name: ").strip()
        if not payee_name:
            print("Payee name cannot be empty!")
            return None
        bank = input("Enter associated bank: ").strip()
        if not bank:
            print("Bank name cannot be empty!")
            return None
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be positive!")
                return None
            remarks = input("Enter remarks: ")
            return MoneyTransfer(payee_name, bank, amount, remarks)
        except ValueError:
            print("Invalid amount!")
            return None
    elif choice == '2':
        bill_category = input("Enter bill category: ").strip()
        if not bill_category:
            print("Bill category cannot be empty!")
            return None
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be positive!")
                return None
            remarks = input("Enter remarks: ")
            return BillPayment(bill_category, amount, remarks)
        except ValueError:
            print("Invalid amount!")
            return None
    elif choice == '3':
        mobile_number = input("Enter mobile number: ").strip()
        if not mobile_number:
            print("Mobile number cannot be empty!")
            return None
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be positive!")
                return None
            remarks = input("Enter remarks: ")
            return MobileRecharge(mobile_number, amount, remarks)
        except ValueError:
            print("Invalid amount!")
            return None
    else:
        print("Invalid choice!")
        return None