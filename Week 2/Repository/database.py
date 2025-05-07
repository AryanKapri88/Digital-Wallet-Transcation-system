import sqlite3

class Database:
    def __init__(self, db_name='payment.db'):
        self.conn = sqlite3.connect(f'repository/{db_name}')
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                              (username TEXT PRIMARY KEY, balance REAL, tier TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions 
                              (transaction_id TEXT PRIMARY KEY, date TEXT, type TEXT, 
                               total_balance REAL, amount REAL, remaining_balance REAL, 
                               remarks TEXT, user_id TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pins 
                              (username TEXT PRIMARY KEY, pin TEXT)''')
        self.conn.commit()

    def save_user(self, username, balance, tier):
        self.cursor.execute("INSERT OR REPLACE INTO users (username, balance, tier) VALUES (?, ?, ?)",
                           (username, balance, tier))
        self.conn.commit()

    def update_user_balance(self, username, balance):
        self.cursor.execute("UPDATE users SET balance = ? WHERE username = ?", (balance, username))
        self.conn.commit()

    def save_transaction(self, transaction):
        self.cursor.execute('''INSERT OR REPLACE INTO transactions 
                              (transaction_id, date, type, total_balance, amount, remaining_balance, remarks, user_id) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (transaction['transaction_id'],
                            transaction['date'].strftime('%Y-%m-%d'),
                            transaction['type'],
                            transaction['total_balance'],
                            transaction['amount'],
                            transaction['remaining_balance'],
                            transaction['remarks'],
                            transaction['user_id']))
        self.conn.commit()

    def save_pin(self, username, pin):
        self.cursor.execute("INSERT OR REPLACE INTO pins (username, pin) VALUES (?, ?)", (username, pin))
        self.conn.commit()

    def get_pin(self, username):
        self.cursor.execute("SELECT pin FROM pins WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()