import os
import asyncio
import sqlite3
from pathlib import Path
import util.pasync as pasync

_conn: sqlite3.Connection = None

class Data:

    @staticmethod
    async def init(path: str):
        global _conn
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(path, isolation_level=None, check_same_thread=False)

        con.execute("""CREATE TABLE IF NOT EXISTS UsersBalance (server_id INTEGER, user_id INTEGER, balance INTEGER DEFAULT 0)""")
        con.execute("""CREATE TABLE IF NOT EXISTS Users (server_id INTEGER, user_id INTEGER, message INTEGER DEFAULT 0, voice_activ INTEGER DEFAULT 0, warns INTEGER DEFAULT 0, lvl INTEGER DEFAULT 1, xp INTEGER DEFAULT 0)""")
        con.execute("""CREATE TABLE IF NOT EXISTS VoiceMaster (server_id INTEGER, user_id INTEGER, channel_id, json TEXT)""")
        con.execute("""CREATE TABLE IF NOT EXISTS Love (server_id INTEGER, user_id INTEGER, member_love, json TEXT)""")
        con.execute("""CREATE TABLE IF NOT EXISTS Role (id INTEGER,server_id INTEGER NOT NULL,user_id INTEGER NOT NULL, role_id INTEGER NOT NULL,price INTEGER NOT NULL);""")
        con.execute("""CREATE TABLE IF NOT EXISTS TimeOut (server_id INTEGER NOT NULL, user_id INTEGER NOT NULL, json TEXT, PRIMARY KEY (server_id, user_id));""")

        con.execute('''CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                thread_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
        
        Data.users = Teable("Users")
        Data.usersBalance = Teable("UsersBalance")
        Data.voiceMaster = Teable("VoiceMaster")
        Data.love = Teable("Love")
        Data.role = Teable("Role")
        Data.timeOut = Teable("TimeOut")
        Data.tickets = Teable("tickets")

        con.commit()

        _conn = con

    @staticmethod
    def get_cur():
        return _conn.cursor()

    @staticmethod
    def commit():
        _conn.commit()

class TeableLock(pasync.Lock):
    def __init__(self):
        super().__init__()
        self._owner = None

    async def acquire(self):
        await super().acquire()
        self._owner = asyncio.current_task()

    def release(self):
        if self._owner != asyncio.current_task():
            raise RuntimeError("Only lock owner can release it")
        super().release()
        self._owner = None

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.release()

    def try_acquire(self):
        if not self._lock.locked():
            self._loop.call_soon_threadsafe(self._lock.acquire)
            self._owner = asyncio.current_task()
            return True
        return False
    
    def unclock(self):
        return self._UnclockContext(self)

    class _UnclockContext:
        def __init__(self, lock):
            self._lock = lock

        async def __aenter__(self):
            if self._lock._owner != asyncio.current_task():
                raise RuntimeError("Only lock owner can unclock")
            self._lock.release()
            self._lock._owner = None
            await asyncio.sleep(0)

        async def __aexit__(self, exc_type, exc, tb):
            await self._lock.acquire()
            self._lock._owner = asyncio.current_task()

    
_lock = asyncio.Lock()

class Teable(TeableLock):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    async def __aenter__(self):
        await super().__aenter__()
        self.cur = Data.get_cur()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        self.cur.close()
        await super().__aexit__(exc_type, exc, tb)

    def __getattr__(self, name):
        return getattr(self.cur, name)
    
    async def commit(self):
        async with _lock:
            _conn.commit()


class Entry:
    def __init__(self):
        pass