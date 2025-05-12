from Models.user import User

class CLIObserver:
    def update(self, message):
        print(f"Notification: {message}")

def display_create_user_prompt(db):
    username = input("Enter username: ").strip()
    while not username:
        print("Username cannot be empty!")
        username = input("Enter username: ").strip()

    _, cursor = db.conn_mgr.get_connection()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if not existing_user:
        pin = input("Set your 4-digit PIN: ")
        while not (pin.isdigit() and len(pin) == 4):
            print("PIN must be a 4-digit number!")
            pin = input("Set your 4-digit PIN: ")
        db.save_pin(username, pin)

    try:
        initial_balance = float(input("Enter initial balance: "))
        if initial_balance < 0:
            print("Initial balance cannot be negative!")
            initial_balance = float(input("Enter initial balance: "))
    except ValueError:
        print("Invalid balance! Setting to 0.")
        initial_balance = 0.0

    print("Choose user tier: 1. Basic 2. Premium")
    choice = input("Enter choice (1 or 2): ").strip()
    while choice not in ['1', '2']:
        print("Invalid choice! Please enter 1 or 2.")
        choice = input("Enter choice (1 or 2): ").strip()

    return username, initial_balance, choice

def display_main_menu(user):
    print(f"\nWelcome {user.get_username()}! Balance: {user.balance}")
    print("1. Perform Transaction")
    print("2. Exit")
    return input("Enter choice (1 or 2): ").strip()

def display_invalid_choice():
    print("Invalid choice! Please try again.")

def display_exit_message():
    print("Thank you for using the Payment System. Goodbye!")