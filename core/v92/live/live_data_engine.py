from pathlib import Path
from datetime import datetime
import pandas as pd

class V92LiveDataEngine:
    """
    V9.2 Live Data Engine

    数据优先级：
    1. AKShare live adapter（如已安装 akshare）
    2. data/realtime/quotes_realtime.csv
    3. data/inbox/quotes.csv
    4. data/quotes.csv

    说明：
    - 当前先做安全适配层，不强制安装第三方行情库。
    - 如果本地已安装 akshare，可尝试读取 A股实时行情。
    """
    def __init__(self):
        self.csv_sources = [
            ("Realtime CSV", Path("data/realtime/quotes_realtime.csv")),
            ("Inbox CSV", Path("data/inbox/quotes.csv")),
            ("Local CSV", Path("data/quotes.csv")),
        ]

    def _normalize(self, df, source):
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        rename_map = {
            "代码": "code",
            "名称": "name",
            "最新价": "price",
            "涨跌幅": "change_pct",
            "成交额": "amount",
            "成交量": "volume",
            "换手率": "turnover",
        }
        df = df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns})
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0","",regex=False).str.zfill(6)
        for col in ["price","change_pct","main_inflow","trend","capital","risk","quality","lia","amount","volume","turnover"]:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        if "name" not in df.columns:
            df["name"] = df.get("code", "")
        df["source"] = source
        df["loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df

    def _akshare_quotes(self):
        try:
            import akshare as ak
            raw = ak.stock_zh_a_spot_em()
            return self._normalize(raw, "AKShare EastMoney")
        except Exception as e:
            return pd.DataFrame(), str(e)

    def get_quotes(self, prefer_live=True):
        if prefer_live:
            live = self._akshare_quotes()
            if isinstance(live, tuple):
                live_df, err = live
            else:
                live_df, err = live, None
            if live_df is not None and not live_df.empty:
                return live_df

        for name, path in self.csv_sources:
            if path.exists():
                try:
                    df = pd.read_csv(path)
                    df = self._normalize(df, name)
                    if not df.empty:
                        return df
                except Exception:
                    continue
        return pd.DataFrame()

    def health(self):
        live_ok = False
        live_error = None
        try:
            import akshare as ak
            live_ok = True
        except Exception as e:
            live_error = str(e)

        csv_rows = []
        for name, path in self.csv_sources:
            rows = 0
            updated = None
            exists = path.exists()
            if exists:
                try:
                    rows = len(pd.read_csv(path))
                    updated = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    updated = f"ERROR: {e}"
            csv_rows.append({"source": name, "exists": exists, "rows": rows, "updated": updated, "path": str(path)})

        q = self.get_quotes(prefer_live=True)
        active = q["source"].iloc[0] if not q.empty and "source" in q.columns else "WAITING_DATA"

        return {
            "engine": "V9.2 Live Data Engine",
            "akshare_installed": live_ok,
            "akshare_error": live_error,
            "active_source": active,
            "rows": len(q),
            "live_ready": active == "AKShare EastMoney",
            "csv_sources": csv_rows,
        }
