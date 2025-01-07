from util.db import *

class TimeOut(DBWapper):
    
    @staticmethod
    def getTimeOut(server_id, user_id):
        result = TimeOut.execute(
            "SELECT json FROM TimeOut WHERE server_id = ? AND user_id = ?",
            (server_id, user_id)
        ).fetchone()
        return result[0] if result else None

    @staticmethod
    def addTimeOut(server_id, user_id, timeout_data):
        existing_record = TimeOut.execute(
            "SELECT json FROM TimeOut WHERE server_id = ? AND user_id = ?",
            (server_id, user_id)
        ).fetchone()

        if existing_record:
            TimeOut.updateTimeOut(server_id, user_id, timeout_data)
        else:
            TimeOut.execute(
                "INSERT INTO TimeOut (server_id, user_id, json) VALUES (?, ?, ?)",
                (server_id, user_id, timeout_data)
            )
            TimeOut.commit()

    @staticmethod
    def updateTimeOut(server_id, user_id, timeout_data):
        TimeOut.execute(
            "UPDATE TimeOut SET json = ? WHERE server_id = ? AND user_id = ?",
            (timeout_data, server_id, user_id)
        )
        TimeOut.commit()

    @staticmethod
    def removeTimeOut(server_id, user_id):
        TimeOut.execute(
            "DELETE FROM TimeOut WHERE server_id = ? AND user_id = ?",
            (server_id, user_id)
        )
        TimeOut.commit()