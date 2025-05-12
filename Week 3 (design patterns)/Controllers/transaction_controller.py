from Models.transaction import MoneyTransfer, BillPayment, MobileRecharge

class TransactionFactory:
    @staticmethod
    def create_transaction(choice):
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

def perform_transaction(user):
    print("\nChoose transaction type: 1. Money Transfer 2. Bill Payment 3. MobileRecharge")
    choice = input("Enter choice (1, 2, or 3): ")
    transaction = TransactionFactory.create_transaction(choice)
    return transaction

def save_statement(transactions, username, db):
    if not transactions:
        return

    for transaction in transactions:
        db.save_transaction(transaction)
    print(f"Transaction statement saved to database for user {username}")