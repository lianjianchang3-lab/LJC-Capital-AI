from core.morning import MorningBrief


def test_morning_brief():
    data = MorningBrief().generate()
    assert "market" in data
    assert "position" in data
    assert "diamond" in data
