from pathlib import Path
from datetime import datetime
import pandas as pd
import requests
import random
import time

class MultiSourceRealtimeHub:
    """
    周一可用多源行情：
    1 AKShare/东方财富
    2 新浪行情：重点股票池实时
    3 腾讯行情：重点股票池实时
    4 CSV缓存兜底
    """
    WATCHLIST = {
        "300136": "信维通信",
        "300762": "上海瀚讯",
        "603308": "应流股份",
        "688008": "澜起科技",
        "688387": "信科移动",
        "300059": "东方财富",
        "300342": "天银机电",
        "688568": "中科星图",
    }

    def __init__(self):
        self.cache = Path("data/realtime/multisource_quotes_cache.csv")
        self.csv_sources = [
            ("多源缓存", self.cache),
            ("Monday缓存", Path("data/realtime/monday_quotes_cache.csv")),
            ("V10.5缓存", Path("data/realtime/v105_live_cache.csv")),
            ("V101缓存", Path("data/realtime/v101_quotes_cache.csv")),
            ("实时CSV", Path("data/realtime/quotes_realtime.csv")),
            ("导入CSV", Path("data/inbox/quotes.csv")),
            ("本地CSV", Path("data/quotes.csv")),
        ]

    def _prefix_sina(self, code):
        if str(code).startswith(("6", "9")):
            return "sh" + str(code)
        return "sz" + str(code)

    def _prefix_tencent(self, code):
        if str(code).startswith(("6", "9")):
            return "sh" + str(code)
        return "sz" + str(code)

    def _normalize(self, df, source):
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        rename = {
            "代码":"code","名称":"name","最新价":"price","涨跌幅":"change_pct","成交额":"amount",
            "成交量":"volume","换手率":"turnover","总市值":"market_cap","市盈率-动态":"pe"
        }
        df = df.rename(columns={k:v for k,v in rename.items() if k in df.columns})
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0","",regex=False).str.zfill(6)
        if "name" not in df.columns:
            df["name"] = df["code"] if "code" in df.columns else ""
        if "sector" not in df.columns:
            df["sector"] = "重点观察"
        for c in ["price","change_pct","amount","volume","turnover","main_inflow","trend","capital","risk","quality","lia","market_cap","pe"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        df["source"] = source
        df["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df

    def fetch_akshare(self):
        try:
            import os
            os.environ["NO_PROXY"] = "*"
            os.environ["no_proxy"] = "*"
            import akshare as ak
            df = ak.stock_zh_a_spot_em()
            df = self._normalize(df, "AKShare东方财富实时")
            if len(df) > 1000:
                self._save_cache(df)
                return df, None
            return pd.DataFrame(), f"AKShare行数异常：{len(df)}"
        except Exception as e:
            return pd.DataFrame(), str(e)

    def fetch_sina_watchlist(self):
        rows = []
        try:
            codes = ",".join([self._prefix_sina(c) for c in self.WATCHLIST])
            url = "https://hq.sinajs.cn/list=" + codes
            headers = {"Referer": "https://finance.sina.com.cn", "User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=8)
            r.encoding = "gbk"
            text = r.text
            for line in text.split(";"):
                if "hq_str_" not in line or '="' not in line:
                    continue
                sym = line.split("hq_str_")[1].split("=")[0]
                code = sym[-6:]
                data = line.split('="',1)[1].strip('"')
                parts = data.split(",")
                if len(parts) < 32 or not parts[0]:
                    continue
                name = parts[0]
                open_p = float(parts[1] or 0)
                pre_close = float(parts[2] or 0)
                price = float(parts[3] or 0)
                volume = float(parts[8] or 0)
                amount = float(parts[9] or 0)
                pct = ((price - pre_close) / pre_close * 100) if pre_close else 0
                rows.append({"code":code,"name":name,"price":price,"change_pct":round(pct,2),"volume":volume,"amount":amount})
            df = self._normalize(pd.DataFrame(rows), "新浪重点股实时")
            if not df.empty:
                self._save_cache(df)
            return df, None
        except Exception as e:
            return pd.DataFrame(), str(e)

    def fetch_tencent_watchlist(self):
        rows = []
        try:
            codes = ",".join([self._prefix_tencent(c) for c in self.WATCHLIST])
            url = "https://qt.gtimg.cn/q=" + codes
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=8)
            r.encoding = "gbk"
            for line in r.text.split(";"):
                if "~" not in line:
                    continue
                data = line.split('="',1)[-1].strip('"')
                p = data.split("~")
                if len(p) < 38:
                    continue
                code = p[2]
                name = p[1]
                price = float(p[3] or 0)
                pct = float(p[32] or 0) if len(p) > 32 else 0
                volume = float(p[6] or 0)
                amount = float(p[37] or 0) * 10000 if len(p) > 37 else 0
                rows.append({"code":code,"name":name,"price":price,"change_pct":pct,"volume":volume,"amount":amount})
            df = self._normalize(pd.DataFrame(rows), "腾讯重点股实时")
            if not df.empty:
                self._save_cache(df)
            return df, None
        except Exception as e:
            return pd.DataFrame(), str(e)

    def fetch_csv(self):
        last_error = None
        for name, path in self.csv_sources:
            if path.exists():
                try:
                    df = self._normalize(pd.read_csv(path), name)
                    if not df.empty:
                        return df, None
                except Exception as e:
                    last_error = str(e)
        return pd.DataFrame(), last_error or "没有CSV备用数据"

    def _save_cache(self, df):
        Path("data/realtime").mkdir(parents=True, exist_ok=True)
        df.to_csv(self.cache, index=False)

    def quotes(self):
        errors = {}
        for name, func in [
            ("AKShare", self.fetch_akshare),
            ("Sina", self.fetch_sina_watchlist),
            ("Tencent", self.fetch_tencent_watchlist),
            ("CSV", self.fetch_csv),
        ]:
            df, err = func()
            if df is not None and not df.empty:
                df["_provider_chain"] = name
                return df
            errors[name] = err
        df = pd.DataFrame()
        df.attrs["errors"] = errors
        return df

    def score(self):
        df = self.quotes()
        if df.empty:
            return df
        df = df.copy()
        for c in ["change_pct","amount","volume","turnover","main_inflow","trend","capital","risk","lia"]:
            df[c] = pd.to_numeric(df.get(c, 0), errors="coerce").fillna(0)
        df["LJC实时分"] = (
            df["amount"].rank(pct=True)*25 +
            df["volume"].rank(pct=True)*15 +
            df["change_pct"].clip(-10,10)*3 +
            df["turnover"].rank(pct=True)*10 +
            df["lia"]*0.2 +
            df["capital"]*0.2 -
            df["risk"]*0.2
        ).round(1)
        df["AI信号"] = "观察"
        df.loc[(df["LJC实时分"]>=75)&(df["risk"]<=70), "AI信号"] = "买入观察"
        df.loc[(df["LJC实时分"]>=90)&(df["risk"]<=60), "AI信号"] = "重点买入关注"
        df.loc[(df["risk"]>=75)|(df["change_pct"]<=-5), "AI信号"] = "风险回避"
        df["建议仓位"] = "0%-3%"
        df.loc[df["AI信号"]=="买入观察","建议仓位"]="5%-10%"
        df.loc[df["AI信号"]=="重点买入关注","建议仓位"]="10%-15%"
        df.loc[df["AI信号"]=="风险回避","建议仓位"]="0%"
        return df.sort_values("LJC实时分", ascending=False)

    def health(self):
        ak_df, ak_err = self.fetch_akshare()
        sina_df, sina_err = self.fetch_sina_watchlist()
        ten_df, ten_err = self.fetch_tencent_watchlist()
        csv_df, csv_err = self.fetch_csv()
        q = self.quotes()
        source = q["source"].iloc[0] if not q.empty else "无数据"
        return {
            "system": "MultiSource Realtime Fallback",
            "active_source": source,
            "rows": int(len(q)),
            "full_market_ready": int(len(ak_df)) > 1000,
            "watchlist_ready": int(len(sina_df)) > 0 or int(len(ten_df)) > 0,
            "akshare_rows": int(len(ak_df)),
            "akshare_error": ak_err,
            "sina_rows": int(len(sina_df)),
            "sina_error": sina_err,
            "tencent_rows": int(len(ten_df)),
            "tencent_error": ten_err,
            "csv_rows": int(len(csv_df)),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
