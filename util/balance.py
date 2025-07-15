import disnake
import sqlite3

from util.db import Data

class Balance:
    @staticmethod
    async def addBalance(server_id, user_id, cout):
        async with Data.usersBalance as balance:
            balance.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
            row = balance.fetchone()
            if row:
                bal = row[2]
                result = bal + cout
                balance.execute("""UPDATE UsersBalance SET balance = ? WHERE server_id = ? AND user_id = ?""", (result, server_id, user_id))
                await balance.commit()
            else:
                balance.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, ?)""",
                                          (server_id, user_id, cout))
                await balance.commit()
                return cout
        
    @staticmethod
    async def getBalance(server_id, user_id):
        async with Data.usersBalance as balance:
            balance.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
            row = balance.fetchone()
            if row:
                bal = row[2]
                return bal
            else:
                balance.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, 0)""",
                                          (server_id, user_id))
                await balance.commit()
                return 0
    
    @staticmethod
    async def spendBalance(server_id, user_id, count):
        async with Data.usersBalance as balance:
            balance.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
            row = balance.fetchone()
            if row:
                bal = row[2]
                result = bal - count
                balance.execute("""UPDATE UsersBalance SET balance = ? WHERE server_id = ? AND user_id = ?""", (result, server_id, user_id))
                await balance.commit()
            else:
                balance.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, ?)""",
                                (server_id, user_id, count))
                await balance.commit()
                return count

    @staticmethod
    async def setBalance(server_id, user_id, count):
        async with Data.usersBalance as balance:
            balance.execute("SELECT * FROM UsersBalance WHERE server_id = ? AND user_id = ?", (server_id, user_id))
            row = balance.fetchone()
            if row:
                balance.execute("""UPDATE UsersBalance SET balance = ? WHERE server_id = ? AND user_id = ?""", (count, server_id, user_id))
                await balance.commit()
            else:
                balance.execute("""INSERT INTO UsersBalance (server_id, user_id, balance) VALUES (?, ?, ?)""",
                                (server_id, user_id, count))
                await balance.commit()
                return count

    