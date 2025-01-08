import sqlite3

class Data:
    con = sqlite3.connect("data.db")

    @staticmethod
    def getCur():
        return Data.con.cursor()
    #cur.execute("""CREATE TABLE IF NOT EXISTS users(server_id INTEGER, user_id INTEGER, lvl INTEGER DEFAULT 1, xp INTEGER DEFAULT 0, money INTEGER DEFAULT 0)""")

    con.execute("""CREATE TABLE IF NOT EXISTS UsersBalance (server_id INTEGER, user_id INTEGER, balance INTEGER DEFAULT 0)""")
    con.execute("""CREATE TABLE IF NOT EXISTS Users (server_id INTEGER, user_id INTEGER, message INTEGER DEFAULT 0, voice_activ INTEGER DEFAULT 0, warns INTEGER DEFAULT 0, lvl INTEGER DEFAULT 1, xp INTEGER DEFAULT 0)""")
    con.execute("""CREATE TABLE IF NOT EXISTS VoiceMaster (server_id INTEGER, user_id INTEGER, channel_id, json TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS Love (server_id INTEGER, user_id INTEGER, member_love, json TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS Role (id INTEGER,server_id INTEGER NOT NULL,user_id INTEGER NOT NULL, role_id INTEGER NOT NULL,price INTEGER NOT NULL);""")
    con.execute("""CREATE TABLE IF NOT EXISTS TimeOut (server_id INTEGER NOT NULL, user_id INTEGER NOT NULL, json TEXT);""")

    con.commit()

    @staticmethod
    def commit():
        Data.con.commit()


class DBWapper:
    cur = Data.getCur()

    @staticmethod
    def execute(*args):
        return DBWapper.cur.execute(*args)
    
    @staticmethod
    def commit():
        Data.commit()
