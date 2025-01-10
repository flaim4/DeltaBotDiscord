import os.path
import uuid
import traceback
import json
from datetime import datetime
import settings

def save_error_report(exception:Exception, additional_data:dict=None, report_file:str=os.path.join(settings.__work_data__, "error_reports.json")) -> str:
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