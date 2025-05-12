from .connection import ConnectionManager

class TableCreator:
    def __init__(self, conn_mgr: ConnectionManager):
        self.conn, self.cursor = conn_mgr.get_connection()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                              (username TEXT PRIMARY KEY, balance REAL, tier TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions 
                              (transaction_id TEXT PRIMARY KEY, date TEXT, type TEXT, 
                               total_balance REAL, amount REAL, remaining_balance REAL, 
                               remarks TEXT, user_id TEXT, recipient TEXT, transaction_mode TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pins 
                              (username TEXT PRIMARY KEY, pin TEXT)''')
        self.conn.commit()