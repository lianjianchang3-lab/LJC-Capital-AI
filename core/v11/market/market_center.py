import pandas as pd
from core.v11.data.data_center import DataCenterV11

class MarketCenterV11:
    def snapshot(self):
        df = DataCenterV11().quotes()
        if df.empty:
            return {"status":"NO DATA","summary":"等待数据","hot_sectors":[],"leaders":[]}
        for col in ["change_pct","amount","lia","capital","risk"]:
            df[col] = pd.to_numeric(df.get(col,0), errors="coerce").fillna(0)
        up = int((df["change_pct"] > 0).sum())
        down = int((df["change_pct"] < 0).sum())
        hot = []
        if "sector" in df.columns:
            g = df.groupby("sector").agg(股票数=("code","count"),平均涨幅=("change_pct","mean"),成交额=("amount","sum"),平均LIA=("lia","mean")).reset_index()
            g["市场热度"] = (g["平均涨幅"].clip(-10,10)*2 + g["成交额"].rank(pct=True)*30 + g["平均LIA"]*0.3).round(1)
            hot = g.sort_values("市场热度", ascending=False).head(10).to_dict("records")
        leaders = df.sort_values(["lia","capital","amount"], ascending=False).head(10).to_dict("records")
        return {"status":"OK","summary":f"上涨{up}，下跌{down}，总样本{len(df)}","up_count":up,"down_count":down,"hot_sectors":hot,"leaders":leaders}
