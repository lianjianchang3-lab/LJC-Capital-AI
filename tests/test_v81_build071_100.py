from core.commander import CommanderCenter
from core.trading_plan import TradingPlanEngine
from core.alerts import AlertCenter
from core.official import OfficialValidation

def test_commander():
    assert "final_decision" in CommanderCenter().snapshot()

def test_trading_alert_validation():
    assert "plans" in TradingPlanEngine().generate()
    assert "alerts" in AlertCenter().scan()
    assert "checks" in OfficialValidation().validate()
