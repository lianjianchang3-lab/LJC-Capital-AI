from pathlib import Path
from datetime import datetime
from core.v11.data.data_center import DataCenterV11
from core.v11.ai.ai_center import AICenterV11
from core.v11.risk.risk_center import RiskCenterV11

class SystemCenterV11:
    def status(self):
        return {"version":"V11 RC1","time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"data":DataCenterV11().health(),"ai":AICenterV11().decisions().get("status"),"risk":RiskCenterV11().assess().get("status"),"config_exists":Path("config").exists(),"logs_exists":Path("logs").exists(),"plugins_exists":Path("plugins").exists()}
