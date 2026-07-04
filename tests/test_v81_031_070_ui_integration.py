from pathlib import Path

def test_app_contains_strategy_workbench():
    text = Path("app.py").read_text(encoding="utf-8")
    assert "Build031-070 Strategy Workbench" in text
    assert "MasterStrategyV3" in text
    assert "WorkbenchEngine" in text
