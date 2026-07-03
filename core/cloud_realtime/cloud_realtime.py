from datetime import datetime
import pandas as pd

from core.data_center import DataCenter
from core.realtime.providers import SinaRealtimeProvider


class CloudRealtimeService:
    '''
    V8.2 Build002 Pure Cloud Realtime

    Streamlit Cloud / 手机端直接抓公开行情快照。
    不依赖 Mac 本地更新 quotes.csv。
    注意：这是公开行情快照，不是 Level-2 或逐笔资金。
    '''

    def __init__(self, data_center=None):
        self.dc = data_center or DataCenter()
        self.provider = SinaRealtimeProvider()

    def watchlist_codes(self):
        watch = self.dc.get_watchlist().data
        if watch.empty or "code" not in watch.columns:
            return []
        return [str(x).zfill(6) for x in watch["code"].tolist()]

    def fetch_live_quotes(self, codes=None):
        codes = codes or self.watchlist_codes()
        if not codes:
            return pd.DataFrame(), {
                "ok": False,
                "message": "没有自选股代码。",
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        try:
            df = self.provider.fetch_quotes(codes)
            return df, {
                "ok": not df.empty,
                "message": "云端实时行情已获取" if not df.empty else "云端实时行情为空",
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rows": len(df),
                "source": "sina_public_cloud",
            }
        except Exception as e:
            return pd.DataFrame(), {
                "ok": False,
                "message": f"云端行情获取失败：{e}",
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rows": 0,
                "source": "sina_public_cloud",
            }

    def merge_with_lia(self, signals):
        live_df, status = self.fetch_live_quotes([s.code for s in signals])
        if live_df.empty:
            return [], status

        by_code = {str(r["code"]).zfill(6): r for _, r in live_df.iterrows()}
        rows = []
        for s in signals:
            q = by_code.get(str(s.code).zfill(6), {})
            rows.append({
                "代码": s.code,
                "名称": s.name,
                "实时价": q.get("close", None),
                "涨跌幅": q.get("change_pct", None),
                "成交额(亿)": q.get("turnover", None),
                "行情时间": q.get("time", ""),
                "LIA": s.lia,
                "资金": s.capital,
                "评级": s.rank,
                "建议": s.action,
            })
        return rows, status
