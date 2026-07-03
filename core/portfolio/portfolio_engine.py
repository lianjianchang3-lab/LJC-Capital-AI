from pathlib import Path
import pandas as pd
from core.lia import LIAEngine


class PortfolioEngine:
    def __init__(self, path="data/portfolio.csv", lia_engine=None):
        self.path = Path(path)
        self.lia_engine = lia_engine or LIAEngine()

    def _ensure_sample(self):
        if self.path.exists():
            return
        self.path.parent.mkdir(exist_ok=True)
        self.path.write_text(
            "code,name,shares,cost\n"
            "300136,信维通信,1000,98.0\n"
            "300762,上海瀚讯,1000,62.0\n",
            encoding="utf-8",
        )

    def load(self):
        self._ensure_sample()
        return pd.read_csv(self.path, dtype={"code": str})

    def analyze(self):
        df = self.load()
        rows = []
        for _, row in df.iterrows():
            code = str(row["code"]).zfill(6)
            sig = self.lia_engine.analyze(code)
            rows.append({
                "代码": code,
                "名称": row.get("name", sig.name),
                "持仓": row.get("shares", 0),
                "成本": row.get("cost", 0),
                "LIA": sig.lia,
                "评级": sig.rank,
                "建议": sig.action,
                "说明": sig.explanation,
            })
        return pd.DataFrame(rows)
