from Models.payment import PaymentProcessor
from Views.cli import (
    display_create_user_prompt, display_main_menu, display_invalid_choice, display_exit_message, CLIObserver
)
from Controllers.user_controller import create_user
from Controllers.transaction_controller import perform_transaction, save_statement
from Repository.database import Database

class PaymentSystemFacade:
    def __init__(self):
        self.db = Database.get_instance()
        self.processor = PaymentProcessor(self.db)
        self.observer = CLIObserver()
        self.processor.register_observer(self.observer)

    def create_user(self, username, initial_balance, choice):
        return create_user(username, initial_balance, choice, self.db)

    def perform_transaction(self, user):
        transaction = perform_transaction(user)
        if transaction is not None:
            success, new_user = self.processor.process_transaction(user, transaction)
            if success:
                user = new_user
                save_statement(self.processor.get_transactions(), user.get_username(), self.db)
        return user

    def save_and_exit(self, user):
        save_statement(self.processor.get_transactions(), user.get_username(), self.db)
        display_exit_message()

    def close(self):
        self.db.close()

def main():
    facade = PaymentSystemFacade()
    username, initial_balance, choice = display_create_user_prompt(facade.db)
    user = facade.create_user(username, initial_balance, choice)

    while True:
        choice = display_main_menu(user)
        if choice == '1':
            user = facade.perform_transaction(user)
        elif choice == '2':
            facade.save_and_exit(user)
            break
        else:
            display_invalid_choice()
    facade.close()

if __name__ == "__main__":
    main()