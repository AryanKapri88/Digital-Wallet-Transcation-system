from datetime import datetime

class Transaction:
    def __init__(self, amount, remarks):
        self.amount = amount
        self.remarks = remarks
        self.date = datetime.now()

    def get_transaction_type(self):
        return "Generic Transaction"

    def get_details(self):
        return f"Amount: {self.amount}, Remarks: {self.remarks}"

class MoneyTransfer(Transaction):
    def __init__(self, payee_name, bank, amount, remarks):
        super().__init__(amount, remarks)
        self.payee_name = payee_name
        self.bank = bank

    def get_transaction_type(self):
        return "Money Transfer"

    def get_details(self):
        return f"Payee: {self.payee_name}, Bank: {self.bank}, Amount: {self.amount}, Remarks: {self.remarks}"

class BillPayment(Transaction):
    def __init__(self, bill_category, amount, remarks):
        super().__init__(amount, remarks)
        self.bill_category = bill_category

    def get_transaction_type(self):
        return "Bill Payment"

    def get_details(self):
        return f"Bill Category: {self.bill_category}, Amount: {self.amount}, Remarks: {self.remarks}"

class MobileRecharge(Transaction):
    def __init__(self, mobile_number, amount, remarks):
        super().__init__(amount, remarks)
        self.mobile_number = mobile_number

    def get_transaction_type(self):
        return "Mobile Recharge"

    def get_details(self):
        return f"Mobile Number: {self.mobile_number}, Amount: {self.amount}, Remarks: {self.remarks}"