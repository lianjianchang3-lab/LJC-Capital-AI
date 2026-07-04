from pathlib import Path
from datetime import datetime
import pandas as pd

class RealtimeCore:
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
        rename = {"代码":"code","名称":"name","最新价":"price","涨跌幅":"change_pct","成交额":"amount","成交量":"volume","换手率":"turnover"}
        df = df.rename(columns={k:v for k,v in rename.items() if k in df.columns})
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0", "", regex=False).str.zfill(6)
        if "name" not in df.columns:
            df["name"] = df["code"] if "code" in df.columns else ""
        for col in ["price","change_pct","amount","volume","turnover","main_inflow","trend","capital","risk","quality","lia"]:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        df["source"] = source
        df["loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df

    def _akshare(self):
        try:
            import akshare as ak
            raw = ak.stock_zh_a_spot_em()
            return self._normalize(raw, "AKShare-EastMoney"), None
        except Exception as e:
            return pd.DataFrame(), str(e)

    def _csv(self):
        errors = []
        for name, path in self.csv_sources:
            if not path.exists():
                continue
            try:
                df = pd.read_csv(path)
                df = self._normalize(df, name)
                if not df.empty:
                    return df, None
            except Exception as e:
                errors.append(f"{name}: {e}")
        return pd.DataFrame(), "; ".join(errors) if errors else "no csv data"

    def quotes(self, prefer_live=True):
        if prefer_live:
            df, _ = self._akshare()
            if not df.empty:
                self.cache(df)
                return df
        df, _ = self._csv()
        return df

    def cache(self, df):
        Path("data/realtime").mkdir(parents=True, exist_ok=True)
        out = Path("data/realtime/quotes_realtime.csv")
        df.to_csv(out, index=False)
        return str(out)

    def health(self):
        ak_ok = False
        ak_err = None
        try:
            import akshare  # noqa
            ak_ok = True
        except Exception as e:
            ak_err = str(e)
        csv_status = []
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
            csv_status.append({"source": name, "exists": exists, "rows": rows, "updated": updated, "path": str(path)})
        q = self.quotes(prefer_live=True)
        active = q["source"].iloc[0] if not q.empty and "source" in q.columns else "WAITING_DATA"
        return {
            "engine": "V9.3 Realtime Core",
            "akshare_installed": ak_ok,
            "akshare_error": ak_err,
            "active_source": active,
            "rows": len(q),
            "live_ready": active == "AKShare-EastMoney",
            "csv_sources": csv_status,
        }
