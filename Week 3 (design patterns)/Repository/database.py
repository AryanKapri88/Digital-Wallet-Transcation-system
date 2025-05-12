from .connection import ConnectionManager
from .table_setup import TableCreator
from .user_ops import UserOperations
from .transaction_ops import TransactionOperations
from .pin_ops import PinOperations

class Database:
    _instance = None

    @staticmethod
    def get_instance(db_name='payment.db'):
        if Database._instance is None:
            Database._instance = Database(db_name)
        return Database._instance

    def __init__(self, db_name='payment.db'):
        if Database._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")
        self.conn_mgr = ConnectionManager.get_instance(db_name)
        self.table_creator = TableCreator(self.conn_mgr)
        self.user_ops = UserOperations(self.conn_mgr)
        self.trans_ops = TransactionOperations(self.conn_mgr)
        self.pin_ops = PinOperations(self.conn_mgr)
        self.table_creator.create_tables()

    def save_user(self, username, balance, tier):
        self.user_ops.save_user(username, balance, tier)

    def update_user_balance(self, username, balance):
        self.user_ops.update_user_balance(username, balance)

    def save_transaction(self, transaction):
        self.trans_ops.save_transaction(transaction)

    def save_pin(self, username, pin):
        self.pin_ops.save_pin(username, pin)

    def get_pin(self, username):
        return self.pin_ops.get_pin(username)

    def close(self):
        self.conn_mgr.close()