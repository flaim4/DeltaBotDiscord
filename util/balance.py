import disnake
import sqlite3

class Balance:
    con = sqlite3.connect("balance.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS UsersBalance (server_id INTEGER, user_id INTEGER, balance INTEGER DEFAULT 0)""")

    @staticmethod
    def addBalance(server_id, user_id, cout):
        Balance.cur.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Balance.cur.fetchone()
        if row:
            bal = row[2]
            result = bal + cout
            Balance.cur.execute("""UPDATE UsersBalance SET balance = ? WHERE server_id = ? AND user_id = ?""", (result, server_id, user_id))
            Balance.con.commit()
        else: 
            Balance.cur.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, ?)""",
                            (server_id, user_id, cout))
            Balance.con.commit()
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
            Balance.con.commit()
            return 0
    
    @staticmethod
    def spendBalance(server_id, user_id, count):
        Balance.cur.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Balance.cur.fetchone()
        if row:
            bal = row[2]
            result = bal - count
            Balance.cur.execute("""UPDATE UsersBalance SET balance = ? WHERE server_id = ? AND user_id = ?""", (result, server_id, user_id))
            Balance.con.commit()
        else:
            Balance.cur.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, ?)""",
                            (server_id, user_id, count))
            Balance.con.commit()
            return count

    @staticmethod
    def setBalance(server_id, user_id, count):
        Balance.cur.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Balance.cur.fetchone()
        if row:
            Balance.cur.execute("""UPDATE UsersBalance SET balance = ? WHERE server_id = ? AND user_id = ?""", (count, server_id, user_id))
            Balance.con.commit()
        else:
            Balance.cur.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, ?)""",
                            (server_id, user_id, count))
            Balance.con.commit()
            return count

    