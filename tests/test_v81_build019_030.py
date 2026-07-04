from core.ui import CommercialUIData

def test_commercial_ui_data():
    ui = CommercialUIData()
    assert "market_status" in ui.committee_summary()
    assert "suggested_position" in ui.position_dashboard()
    assert "status" in ui.risk_center()
