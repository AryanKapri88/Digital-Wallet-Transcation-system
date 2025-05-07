
# Overview

This is an advanced Python-based payment system implementing the Model-View-Controller (MVC) architectural pattern. It includes features like transaction limits, loan options, user tier upgrades, and PIN-protected transactions.


# Features


`User Management:` Supports creation of Basic and Premium users with an initial balance, stored in a SQLite database.



`Transaction Types:` Supports Money Transfer, Bill Payment, and Mobile Recharge transactions, with details saved to the database.



`Transaction Limits:` Basic users are limited to 5 transactions per day.



`Loan Option:` Users can take a loan with 5% annual interest if their balance is insufficient.



`Upgrade Option:` Basic users can upgrade to Premium by paying a subscription fee (1000 units).



`PIN Protection:` Transactions require a 4-digit PIN, stored securely in the database.



`Persistent Storage:` Uses SQLite to save user data, transaction history, and PINs in repository/payment.db.


# Project Structure


`main.py:` Entry point of the application, coordinating the MVC components.



`controllers/:` Contains logic for user creation and transaction processing.


    user_controller.py: Handles user creation logic.
    

    transaction_controller.py: Manages transaction execution and statement saving.



`models/:` Defines the data models and business logic.


    user.py: Implements the User, BasicUser, and PremiumUser classes with balance management.


    payment.py: Handles transaction processing and PIN verification.


    transaction.py: Defines transaction types (MoneyTransfer, BillPayment, MobileRecharge).



`views/:` Manages user interface interactions.


    ui.py: Provides prompts, menus, and messages for user input/output.



`repository/:` Manages database interactions.


    database.py: Implements SQLite database operations (saving users, transactions, PINs).
    

    __init__.py: Makes repository a Python package.
