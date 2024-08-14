import sqlite3
import disnake

class Member:
    con = sqlite3.connect("member.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Users (server_id INTEGER, user_id INTEGER, message INTEGER DEFAULT 0, voice_activ INTEGER DEFAULT 0, warns INTEGER DEFAULT 0, lvl INTEGER DEFAULT 1, xp INTEGER DEFAULT 0)""")
    con.commit()
    
    @staticmethod
    def getCountMessage(server_id, user_id):
        Member.cur.execute("SELECT * FROM Users WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Member.cur.fetchone()
        if row:
            return row[2]
        else: 
            Member.cur.execute("""INSERT INTO Users (server_id, user_id, message) VALUES (?, ?, ?)""",
                            (server_id, user_id, 0))
            Member.con.commit()
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
            Member.con.commit()
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

