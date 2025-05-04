# Overview

This is a simple Python-based digital wallet system that allows users to perform transactions like money transfers, bill payments, and mobile recharges. Users can manage their balance, take loans if needed, and track transactions via a CSV file.

# Features

### User Tiers:

    Basic User: Limited to 5 transactions per day, can upgrade to Premium.

    Premium User: Unlimited transactions, requires a one-time subscription fee of 1000.


### Transaction Types:

    Money Transfer: Send money to a payee with a specified bank.

    Bill Payment: Pay bills for categories like electricity.

    TopUp: Recharge your mobile balance via topup.


### PIN Verification:

    Set a 4-digit PIN during setup.

    Verify PIN for each transaction (3 attempts allowed).


### Balance Management:

    Add balance manually if insufficient.

    Option to take a loan with 5% annual interest if balance is low.



### Loan Handling:

    Take a loan to cover transactions.

    Loan details (amount, monthly repayment) are displayed.


### Transaction Limits:

    Basic users are restricted to 5 transactions per day.

    Upgrade to Premium to remove limits.


### Transaction Statement (CSV):

    Saves transactions to transaction.csv.

    Columns: Transaction ID, Date, Transaction Type, Total Balance, Amount, Remaining Balance, Remarks.


# Files


`main.ipynb:` Main script to run the application (Jupyter Notebook).


`user_tier.py:` Handles user tiers (Basic and Premium) and balance management.


`payment_processing.py:` Processes transactions, verifies PIN, and saves to CSV.


`transaction_type.py:` Defines transaction types (Money Transfer, Bill Payment, Mobile Recharge).

