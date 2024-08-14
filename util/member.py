import sqlite3
import disnake

from util.db import Data

class Member:
    cur = Data.getCur()
    
    @staticmethod
    def getCountMessage(server_id, user_id):
        Member.cur.execute("SELECT * FROM Users WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Member.cur.fetchone()
        if row:
            return row[2]
        else: 
            Member.cur.execute("""INSERT INTO Users (server_id, user_id, message) VALUES (?, ?, ?)""",
                            (server_id, user_id, 0))
            Data.commit()
            return 0


    @staticmethod
    def getWarns(server_id, user_id):
        Member.cur.execute("SELECT * FROM Users WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Member.cur.fetchone()
        if row:
            return row[4]
        else: 
            Member.cur.execute("""INSERT INTO Users (server_id, user_id, warns) VALUES (?, ?, ?)""",
                            (server_id, user_id, 0))
            Data.commit()
            return 0

    @staticmethod
    def getCountSecondVoice(server_id, user_id):
        Member.cur.execute("SELECT * FROM Users WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Member.cur.fetchone()
        if row:
            return row[3]
        else: 
            Member.cur.execute("""INSERT INTO Users (server_id, user_id, voice_activ) VALUES (?, ?, ?)""",
                            (server_id, user_id, 0))
            Data.commit()
            return 0
        
    @staticmethod
    def convert_seconds(seconds):
        days = seconds // 86400
        seconds %= 86400
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        
        return days, hours, minutes, seconds

