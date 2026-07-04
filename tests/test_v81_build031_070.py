from core.strategy_v3 import MasterStrategyV3, EntryExitEngine, ScoreV3
from core.selection import SelectionCenter
from core.portfolio_v3 import PortfolioManagerV3
from core.workbench import WorkbenchEngine

def test_strategy_v3():
    assert "market" in MasterStrategyV3().generate()
    assert isinstance(EntryExitEngine().plans(), list)

def test_score_selection_workbench():
    df = ScoreV3().table()
    assert hasattr(df, "empty")
    assert "status" in SelectionCenter().scan()
    assert "status" in PortfolioManagerV3().analyze()
    assert "strategy" in WorkbenchEngine().daily_plan()
