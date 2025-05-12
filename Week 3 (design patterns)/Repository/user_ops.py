from .connection import ConnectionManager

class UserOperations:
    def __init__(self, conn_mgr: ConnectionManager):
        self.conn, self.cursor = conn_mgr.get_connection()

    def save_user(self, username, balance, tier):
        self.cursor.execute("INSERT OR REPLACE INTO users (username, balance, tier) VALUES (?, ?, ?)",
                           (username, balance, tier))
        self.conn.commit()

    def update_user_balance(self, username, balance):
        self.cursor.execute("UPDATE users SET balance = ? WHERE username = ?", (balance, username))
        self.conn.commit()