from .connection import ConnectionManager

class TransactionOperations:
    def __init__(self, conn_mgr: ConnectionManager):
        self.conn, self.cursor = conn_mgr.get_connection()

    def save_transaction(self, transaction):
        self.cursor.execute('''INSERT OR REPLACE INTO transactions 
                              (transaction_id, date, type, total_balance, amount, remaining_balance, 
                               remarks, user_id, recipient, transaction_mode) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (transaction['transaction_id'],
                            transaction['date'].strftime('%Y-%m-%d'),
                            transaction['type'],
                            transaction['total_balance'],
                            transaction['amount'],
                            transaction['remaining_balance'],
                            transaction['remarks'],
                            transaction['user_id'],
                            transaction['recipient'],
                            transaction['transaction_mode']))
        self.conn.commit()