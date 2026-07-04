from pathlib import Path
from datetime import datetime
import pandas as pd

class MondayRealtimeSystem:
    """
    周一可用实时数据系统：
    1. AKShare 东方财富实时行情
    2. 自动缓存 data/realtime/monday_quotes_cache.csv
    3. 失败后降级到已有CSV
    4. 统一字段输出给手机和电脑端
    """
    def __init__(self):
        self.cache_path = Path("data/realtime/monday_quotes_cache.csv")
        self.csv_sources = [
            ("Monday实时缓存", self.cache_path),
            ("V10.5缓存", Path("data/realtime/v105_live_cache.csv")),
            ("V101缓存", Path("data/realtime/v101_quotes_cache.csv")),
            ("实时CSV", Path("data/realtime/quotes_realtime.csv")),
            ("导入CSV", Path("data/inbox/quotes.csv")),
            ("本地CSV", Path("data/quotes.csv")),
        ]

    def _normalize(self, df, source):
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        rename = {
            "代码": "code",
            "名称": "name",
            "最新价": "price",
            "涨跌幅": "change_pct",
            "成交额": "amount",
            "成交量": "volume",
            "换手率": "turnover",
            "总市值": "market_cap",
            "市盈率-动态": "pe",
        }
        df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0", "", regex=False).str.zfill(6)
        if "name" not in df.columns:
            df["name"] = df["code"] if "code" in df.columns else ""
        if "sector" not in df.columns:
            df["sector"] = "未知"

        numeric = [
            "price", "change_pct", "amount", "volume", "turnover",
            "main_inflow", "trend", "capital", "risk", "quality", "lia",
            "market_cap", "pe"
        ]
        for col in numeric:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        df["source"] = source
        df["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df

    def fetch_akshare(self):
        try:
            import akshare as ak
            raw = ak.stock_zh_a_spot_em()
            df = self._normalize(raw, "AKShare东方财富实时")
            if not df.empty:
                Path("data/realtime").mkdir(parents=True, exist_ok=True)
                df.to_csv(self.cache_path, index=False)
            return df, None
        except Exception as e:
            return pd.DataFrame(), str(e)

    def load_csv_fallback(self):
        for name, path in self.csv_sources:
            if path.exists():
                try:
                    df = self._normalize(pd.read_csv(path), name)
                    if not df.empty:
                        return df, None
                except Exception as e:
                    last_error = str(e)
        return pd.DataFrame(), "没有可用CSV备用数据"

    def quotes(self, prefer_live=True):
        live_error = None
        if prefer_live:
            df, live_error = self.fetch_akshare()
            if not df.empty:
                return df
        df, csv_error = self.load_csv_fallback()
        if not df.empty:
            return df
        return pd.DataFrame()

    def health(self):
        ak_installed = False
        ak_error = None
        try:
            import akshare  # noqa
            ak_installed = True
        except Exception as e:
            ak_error = str(e)

        df = self.quotes(prefer_live=True)
        active = df["source"].iloc[0] if not df.empty and "source" in df.columns else "等待数据"
        cache_exists = self.cache_path.exists()
        cache_updated = None
        if cache_exists:
            cache_updated = datetime.fromtimestamp(self.cache_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        return {
            "system": "LJC Monday Realtime Ready",
            "akshare_installed": ak_installed,
            "akshare_error": ak_error,
            "active_source": active,
            "rows": int(len(df)),
            "live_ready": "AKShare" in str(active),
            "cache_exists": cache_exists,
            "cache_updated": cache_updated,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def score(self):
        df = self.quotes(prefer_live=True)
        if df.empty:
            return df
        df = df.copy()
        for col in ["change_pct", "amount", "turnover", "main_inflow", "trend", "capital", "risk", "lia"]:
            df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

        df["LJC实时分"] = (
            df["amount"].rank(pct=True) * 20
            + df["turnover"].rank(pct=True) * 12
            + df["change_pct"].clip(-10, 10) * 2
            + df["main_inflow"] * 25
            + df["trend"] * 0.18
            + df["capital"] * 0.18
            + df["lia"] * 0.16
            - df["risk"] * 0.18
        ).round(1)

        df["AI信号"] = "观察"
        df.loc[(df["LJC实时分"] >= 85) & (df["risk"] <= 60), "AI信号"] = "重点买入关注"
        df.loc[(df["LJC实时分"] >= 75) & (df["risk"] <= 70), "AI信号"] = "买入观察"
        df.loc[(df["risk"] >= 75) | (df["change_pct"] <= -5), "AI信号"] = "风险回避"

        df["建议仓位"] = "0%-3%"
        df.loc[df["AI信号"] == "买入观察", "建议仓位"] = "5%-10%"
        df.loc[df["AI信号"] == "重点买入关注", "建议仓位"] = "10%-15%"
        df.loc[df["AI信号"] == "风险回避", "建议仓位"] = "0%"

        df["理由"] = df.apply(lambda r: f"实时分={r['LJC实时分']} 涨跌幅={r['change_pct']} 换手={r['turnover']} 风险={r['risk']}", axis=1)
        return df.sort_values("LJC实时分", ascending=False)

    def smoke_test(self):
        h = self.health()
        df = self.quotes(prefer_live=True)
        scored = self.score()
        checks = [
            {"检查项": "AKShare已安装", "通过": bool(h["akshare_installed"]), "说明": h.get("akshare_error")},
            {"检查项": "行情数据可读取", "通过": h["rows"] > 0, "说明": h["rows"]},
            {"检查项": "缓存文件可生成", "通过": bool(h["cache_exists"]) or h["rows"] > 0, "说明": h.get("cache_updated")},
            {"检查项": "评分系统可运行", "通过": not scored.empty and "LJC实时分" in scored.columns, "说明": len(scored)},
        ]
        return {"health": h, "checks": checks}
