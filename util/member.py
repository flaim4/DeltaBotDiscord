import sqlite3
import disnake
import time
import json

from util.db import Data
from util.db import DBWapper

class Member(DBWapper):
    
    @staticmethod
    def getCountMessage(server_id, user_id):
        Member.execute("SELECT * FROM Users WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Member.cur.fetchone()
        if row:
            return row[2]
        else: 
            Member.execute("""INSERT INTO Users (server_id, user_id, message) VALUES (?, ?, ?)""",
                            (server_id, user_id, 0))
            Data.commit()
            return 0


    @staticmethod
    def getWarns(server_id, user_id):
        Member.execute("SELECT * FROM Users WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Member.cur.fetchone()
        if row:
            return row[4]
        else: 
            Member.execute("""INSERT INTO Users (server_id, user_id, warns) VALUES (?, ?, ?)""",
                            (server_id, user_id, 0))
            Data.commit()
            return 0

    @staticmethod
    def getCountSecondVoice(server_id, user_id):
        Member.execute("SELECT * FROM Users WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        row = Member.cur.fetchone()
        if row:
            return row[3]
        else: 
            Member.execute("""INSERT INTO Users (server_id, user_id, voice_activ) VALUES (?, ?, ?)""",
                            (server_id, user_id, 0))
            Data.commit()
            return 0
        
    @staticmethod
    def getLoveMember(server_id, author_id):
        Member.execute("SELECT * FROM Love WHERE server_id = ? AND user_id = ?", (server_id, author_id))
        row = Member.cur.fetchone()
        if row:
            return row[2]
        else:
            Member.execute("SELECT * FROM Love WHERE server_id = ? AND member_love = ?", (server_id, author_id))
            row = Member.cur.fetchone()
            if row:
                return row[1]


    @staticmethod
    def setLoveMember(server_id, user: disnake.Member, love_user: disnake.Member):
        HashMap = {"Registe": time.time(), "TimeVoice": 0}
        Member.execute("""INSERT INTO Love (server_id, user_id, member_love, json) VALUES (?, ?, ?, ?)""",(server_id, user.id, love_user.id, json.dumps(HashMap)))
        Data.commit()

    @staticmethod
    def getLoveMemberDataRegister(server_id, user: disnake.Member):
        if (Member.getLoveMember(server_id, user.id) is not None):
            Member.execute("SELECT * FROM Love WHERE server_id = ? AND user_id = ?", (server_id, user.id))
            row = Member.cur.fetchone()
            if row:
                jsonData = json.loads(row[3])
                print(jsonData.get("Registe"))
                return jsonData.get("Registe")
            else:
                Member.execute("SELECT * FROM Love WHERE server_id = ? AND member_love = ?", (server_id, user.id))
                row = Member.cur.fetchone()
                if row:
                    jsonData = json.loads(row[3])
                    print(jsonData.get("Registe"))
                    return jsonData.get("Registe")


    @staticmethod
    def getLoveMemberTimeVoice(server_id, user: disnake.Member):
        if (Member.getLoveMember(server_id, user.id) is not None):
            Member.execute("SELECT * FROM Love WHERE server_id = ? AND user_id = ?", (server_id, user.id))
            row = Member.cur.fetchone()
            if row:
                jsonData = json.loads(row[3])
                print(jsonData.get("TimeVoice"))
                return jsonData.get("TimeVoice")
            else:
                Member.execute("SELECT * FROM Love WHERE server_id = ? AND member_love = ?", (server_id, user.id))
                row = Member.cur.fetchone()
                if row:
                    jsonData = json.loads(row[3])
                    print(jsonData.get("Registe"))
                    return jsonData.get("TimeVoice")

    @staticmethod
    def convert_seconds(seconds):
        days = seconds // 86400
        seconds %= 86400
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        
        return days, hours, minutes, seconds