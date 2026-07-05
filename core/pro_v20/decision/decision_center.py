import pandas as pd
from core.pro_v20.config.config_center import ProConfigCenter

class ProDecisionCenter:
    def __init__(self):
        self.config = ProConfigCenter()

    def _market_data(self):
        try:
            from core.build006 import Build006Commander
            df = Build006Commander().ljc_score()
            if df is not None and not df.empty:
                return df
        except Exception:
            pass
        try:
            from core.multisource import MultiSourceRealtimeHub
            df = MultiSourceRealtimeHub().score()
            if df is not None and not df.empty:
                return df
        except Exception:
            pass
        return pd.DataFrame()

    def decisions(self):
        df = self._market_data()
        if df.empty:
            return pd.DataFrame()

        weights = self.config.weights()
        df = df.copy()
        for c in ["资金分", "趋势分", "量能分", "风险分", "LJC实时分", "risk", "price", "change_pct"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["LJC Alpha Score"] = (
            df["资金分"] * weights.get("capital", 0.30)
            + df["趋势分"] * weights.get("trend", 0.25)
            + df["量能分"] * weights.get("volume", 0.15)
            + df["风险分"] * weights.get("risk", 0.15)
            + df["LJC实时分"] * weights.get("realtime", 0.15)
        ).round(1)

        df["正式建议"] = "观察"
        df.loc[(df["LJC Alpha Score"] >= 88) & (df["risk"] <= 60), "正式建议"] = "买入关注"
        df.loc[(df["LJC Alpha Score"] >= 75) & (df["risk"] <= 70), "正式建议"] = "小仓观察"
        df.loc[(df["risk"] >= 75) | (df["change_pct"] <= -5), "正式建议"] = "减仓/回避"

        df["正式仓位"] = "0%-3%"
        df.loc[df["正式建议"]=="小仓观察", "正式仓位"] = "3%-8%"
        df.loc[df["正式建议"]=="买入关注", "正式仓位"] = "8%-15%"
        df.loc[df["正式建议"]=="减仓/回避", "正式仓位"] = "0%"

        df["证据"] = df.apply(
            lambda r: f"Alpha={r['LJC Alpha Score']} 资金={r['资金分']} 趋势={r['趋势分']} 量能={r['量能分']} 风险={r['risk']}",
            axis=1
        )
        return df.sort_values("LJC Alpha Score", ascending=False)

    def morning_brief(self):
        df = self.decisions()
        if df.empty:
            return {"status": "NO DATA", "summary": "暂无数据", "top": []}
        avg = round(float(df["LJC Alpha Score"].mean()), 1)
        buy = int((df["正式建议"]=="买入关注").sum())
        watch = int((df["正式建议"]=="小仓观察").sum())
        risk = int((df["正式建议"]=="减仓/回避").sum())
        if avg >= 80:
            position = "70%-85%"
            market = "积极"
        elif avg >= 65:
            position = "45%-65%"
            market = "中性偏多"
        else:
            position = "20%-40%"
            market = "防守"
        return {
            "status": "OK",
            "market_score": avg,
            "market_mode": market,
            "position": position,
            "buy_count": buy,
            "watch_count": watch,
            "risk_count": risk,
            "summary": f"今日市场 {market}，AI均分 {avg}，建议仓位 {position}",
            "top": df.head(10).to_dict("records"),
        }
