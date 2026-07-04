import pandas as pd
from pathlib import Path

class SignalBacktester:
    """
    简化信号回测：
    需要 data/backtest/signals_history.csv
    columns: date,code,signal,entry_price,exit_price
    """
    def __init__(self, path="data/backtest/signals_history.csv"):
        self.path = Path(path)

    def run(self):
        if not self.path.exists():
            return {
                "status": "WAITING_BACKTEST_DATA",
                "instruction": "请准备 data/backtest/signals_history.csv，包含 date,code,signal,entry_price,exit_price",
                "summary": {},
                "trades": [],
            }
        df = pd.read_csv(self.path)
        required = {"date","code","signal","entry_price","exit_price"}
        missing = required - set(df.columns)
        if missing:
            return {"status": "MISSING_COLUMNS", "missing": list(missing), "summary": {}, "trades": []}

        df["entry_price"] = pd.to_numeric(df["entry_price"], errors="coerce")
        df["exit_price"] = pd.to_numeric(df["exit_price"], errors="coerce")
        df = df.dropna(subset=["entry_price","exit_price"])
        df["return"] = df["exit_price"] / df["entry_price"] - 1
        win_rate = float((df["return"] > 0).mean()) if len(df) else 0
        avg_ret = float(df["return"].mean()) if len(df) else 0
        max_loss = float(df["return"].min()) if len(df) else 0
        summary = {
            "trade_count": int(len(df)),
            "win_rate": round(win_rate, 4),
            "avg_return": round(avg_ret, 4),
            "max_single_loss": round(max_loss, 4),
            "total_return_simple": round(float(df["return"].sum()), 4),
        }
        return {"status": "OK", "summary": summary, "trades": df.to_dict("records")}
