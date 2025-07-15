from util.db import *

class TimeOut:
    
    @staticmethod
    async def getTimeOut(server_id, user_id):
        async with Data.timeOut as timeout:
            result = timeout.execute(
                "SELECT json FROM TimeOut WHERE server_id = ? AND user_id = ?",
                (server_id, user_id)
            ).fetchone()
            return result[0] if result else None

    @staticmethod
    async def addTimeOut(server_id, user_id, timeout_data):
        async with Data.timeOut as timeout:
            existing_record = timeout.execute(
                "SELECT json FROM TimeOut WHERE server_id = ? AND user_id = ?",
                (server_id, user_id)
            ).fetchone()

            if existing_record:
                timeout.execute(
                    """INSERT INTO TimeOut (server_id, user_id, json)
                        VALUES (?, ?, ?)
                        ON CONFLICT(server_id, user_id) DO UPDATE SET json = excluded.json""",
                    (server_id, user_id, timeout_data)
                )
                await timeout.commit()
            else:
                timeout.execute(
                    "INSERT INTO TimeOut (server_id, user_id, json) VALUES (?, ?, ?)",
                    (server_id, user_id, timeout_data)
                )
                await timeout.commit()

    @staticmethod
    async def updateTimeOut(server_id, user_id, timeout_data):
        async with Data.timeOut as timeout:
            timeout.execute(
                """INSERT INTO TimeOut (server_id, user_id, json)
                    VALUES (?, ?, ?)
                    ON CONFLICT(server_id, user_id) DO UPDATE SET json = excluded.json""",
                (server_id, user_id, timeout_data)
            )
            await timeout.commit()

    @staticmethod
    async def removeTimeOut(server_id, user_id):
        async with Data.timeOut as timeout:
            timeout.execute(
                "DELETE FROM TimeOut WHERE server_id = ? AND user_id = ?",
                (server_id, user_id)
            )
            await timeout.commit()
