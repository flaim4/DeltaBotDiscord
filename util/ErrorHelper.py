import os.path
import typing
import uuid
import traceback
import json
from datetime import datetime
import disnake

class ErrorReport:
    def __init__(self, exception:Exception, additional_data:dict=None, report_file:str=os.path.join(os.work_dir, "error_reports.json")):
        self.id = str(uuid.uuid4())
        self.exception = exception
        self.additional_data = additional_data
        self.report_file = report_file
        self.child : typing.List[ErrorReport] = []
        self.report = {
            "id": self.id,
            "timestamp": datetime.now().isoformat(),
            "err": str(exception),
            "traceback": traceback.format_exc(),
            "data": additional_data or {}
        }

    def __add__(self, other):
        if isinstance(other, ErrorReport):
            self.child.append(other)
        return self

    def __pos__(self, *args):
        return disnake.Embed(description=f"A bot error occurred,\n error indelifer: {self.id}\ncontact the bot developers at [discord](<https://discord.gg/kJSWvqxtre>)")

    def __neg__(self):
        req = self.report.copy()
        if len(self.child) > 0:
            lss = []
            for rep in self.child:
                lss.append(-rep)
            req["child"] = lss
        return req

    def __call__(self, *args, **kwargs):
        try:
            with open(self.report_file, "a") as f:
                f.write(json.dumps(-self, ensure_ascii=False) + "\n")
        except:
            pass



def save_error_report(exception:Exception, additional_data:dict=None, report_file:str=os.path.join(os.work_dir, "error_reports.json")) -> str:
    report_id = str(uuid.uuid4())
    report = {
        "report_id": report_id,
        "timestamp": datetime.now().isoformat(),
        "error": str(exception),
        "traceback": traceback.format_exc(),
        "additional_data": additional_data or {}
    }
    try:
        with open(report_file, "a") as f:
            f.write(json.dumps(report, ensure_ascii=False) + "\n")
    except Exception as save_exception:
        pass

    return report_id
