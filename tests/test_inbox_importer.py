from pathlib import Path
import pandas as pd
from core.data_import import InboxImporter


def test_importer_detect_quotes(tmp_path):
    inbox = tmp_path / "inbox"
    data = tmp_path / "data"
    processed = tmp_path / "processed"
    inbox.mkdir()
    pd.DataFrame([{"代码": "300136", "名称": "信维通信", "最新价": 100, "涨跌幅": 1.2}]).to_csv(inbox / "quotes.csv", index=False)
    importer = InboxImporter(inbox=str(inbox), data_dir=str(data), processed=str(processed))
    result = importer.import_all()
    assert result[0]["status"] == "imported"
    assert (data / "quotes.csv").exists()
