import disnake
import typing

from utility.db import *
from sqlite3 import *

from disnake.ext import commands

class Balance: 

    con: Connection = get_db()
    cur: Cursor = con.cursor()

    @staticmethod
    def get_balance(member: disnake.Member):
        Balance.cur.execute("""SELECT * FROM Members WHERE server_id = ? AND user_id = ?""", (member.guild.id, member.id))
        row: typing.Any = Balance.cur.fetchone()
        if row:
            return row[2]
        else: 
            Balance.cur.execute("""INSERT INTO Members (server_id, user_id, balance) VALUES (?, ?, ?)""",
                            (member.guild.id, member.id, 0))
            Balance.con.commit()
            return 0