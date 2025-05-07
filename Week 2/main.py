from Models.payment import PaymentProcessor
from Views.cli import (
    display_create_user_prompt, display_main_menu, display_invalid_choice, display_exit_message
)
from Controllers.user_controller import create_user
from Controllers.transaction_controller import perform_transaction, save_statement
from Repository.database import Database

def main():
    db = Database()
    username, initial_balance, choice = display_create_user_prompt()
    user = create_user(username, initial_balance, choice, db)
    processor = PaymentProcessor(db)

    while True:
        choice = display_main_menu(user)
        if choice == '1':
            transaction = perform_transaction(user)
            if transaction is not None:
                success, new_user = processor.process_transaction(user, transaction)
                if success:
                    user = new_user
                    save_statement(processor.get_transactions(), user.get_username(), db)
        elif choice == '2':
            save_statement(processor.get_transactions(), user.get_username(), db)
            display_exit_message()
            break
        else:
            display_invalid_choice()
    db.close()

if __name__ == "__main__":
    main()