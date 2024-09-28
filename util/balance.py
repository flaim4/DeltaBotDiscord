import disnake
import sqlite3

from util.db import Data
from util.db import DBWapper

class Balance(DBWapper):
    @staticmethod
    def addBalance(server_id, user_id, cout):
        Balance.cur.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Balance.cur.fetchone()
        if row:
            bal = row[2]
            result = bal + cout
            Balance.cur.execute("""UPDATE UsersBalance SET balance = ? WHERE server_id = ? AND user_id = ?""", (result, server_id, user_id))
            Data.commit()
        else: 
            Balance.cur.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, ?)""",
                            (server_id, user_id, cout))
            Data.commit()
            return cout
        
    @staticmethod
    def getBalance(server_id, user_id):
        Balance.cur.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Balance.cur.fetchone()
        if row:
            bal = row[2]
            return bal
        else:
            Balance.cur.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, 0)""",
                            (server_id, user_id))
            Data.commit()
            return 0
    
    @staticmethod
    def spendBalance(server_id, user_id, count):
        Balance.cur.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Balance.cur.fetchone()
        if row:
            bal = row[2]
            result = bal - count
            Balance.cur.execute("""UPDATE UsersBalance SET balance = ? WHERE server_id = ? AND user_id = ?""", (result, server_id, user_id))
            Data.commit()
        else:
            Balance.cur.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, ?)""",
                            (server_id, user_id, count))
            Data.commit()
            return count

    @staticmethod
    def setBalance(server_id, user_id, count):
        Balance.cur.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Balance.cur.fetchone()
        if row:
            Balance.cur.execute("""UPDATE UsersBalance SET balance = ? WHERE server_id = ? AND user_id = ?""", (count, server_id, user_id))
            Data.commit()
        else:
            Balance.cur.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, ?)""",
                            (server_id, user_id, count))
            Data.commit()
            return count

    