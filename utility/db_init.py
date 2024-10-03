import sqlite3

con: sqlite3.connect = sqlite3.connect("data.db")

def db_init() -> None:
    con.execute("""CREATE TABLE IF NOT EXISTS Members (server_id INTEGER, user_id INTEGER, balance INTEGER DEFAULT 0, level INTEGER DEFAULT 0, xp INTEGER DEFAULT 0, count_message INTEGER DEFAULT 0, reputation INTEGER DEFAULT 0, active_in_voice INTEGER DEFAULT 0, date_is_join INTEGER DEFAULT 0)""")
    con.execute("""CREATE TABLE IF NOT EXISTS Guilds (server_id INTEGER, count_member INTEGER, owner TEXT, json TEXT)""")
    con.commit()
    