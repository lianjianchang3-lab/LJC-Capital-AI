import pandas as pd

class UnifiedAIEngine:
    def __init__(self):
        from core.pro_v30.signal import SignalCenterV5
        self.signal = SignalCenterV5()

    def run(self):
        df = self.signal.signals()
        if df is None or df.empty:
            return pd.DataFrame()

        df = df.copy()
        for c in ["Alpha2.0", "资金共振", "信号强度", "综合风险", "胜率估计", "change_pct", "price"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        # V4统一分数：市场/趋势近似由Alpha体现，资金单独，风险反向，胜率作为情绪和时机
        df["Unified AI Score"] = (
            df["Alpha2.0"] * 0.30
            + df["资金共振"] * 0.25
            + df["信号强度"] * 0.20
            + (100 - df["综合风险"]) * 0.15
            + df["胜率估计"] * 0.10
        ).round(1)

        df["AI等级"] = "C"
        df.loc[df["Unified AI Score"] >= 70, "AI等级"] = "B"
        df.loc[df["Unified AI Score"] >= 82, "AI等级"] = "A"
        df.loc[df["Unified AI Score"] >= 90, "AI等级"] = "S"

        df["统一建议"] = "观察"
        df.loc[(df["Unified AI Score"] >= 88) & (df["综合风险"] < 55), "统一建议"] = "A类立即关注"
        df.loc[(df["Unified AI Score"] >= 76) & (df["综合风险"] < 65), "统一建议"] = "B类等待回踩"
        df.loc[(df["综合风险"] >= 70) | (df["change_pct"] <= -5), "统一建议"] = "C类回避"

        df["证据链"] = df.apply(
            lambda r: f"AI={r['Unified AI Score']} Alpha={r['Alpha2.0']} 资金={r['资金共振']} 风险={r['综合风险']} 胜率={r['胜率估计']}%",
            axis=1
        )
        return df.sort_values("Unified AI Score", ascending=False)

    def market_state(self):
        df = self.run()
        if df.empty:
            return {"status":"NO DATA","summary":"暂无数据"}
        avg = round(float(df["Unified AI Score"].mean()),1)
        risk = round(float(df["综合风险"].mean()),1)
        a_count = int((df["统一建议"]=="A类立即关注").sum())
        c_count = int((df["统一建议"]=="C类回避").sum())

        if avg >= 82 and risk < 50:
            state = "进攻"
            position = "65%-80%"
        elif avg >= 68 and risk < 65:
            state = "震荡偏强"
            position = "45%-65%"
        else:
            state = "防守"
            position = "20%-40%"
        return {
            "status":"OK",
            "ai_score": avg,
            "risk": risk,
            "state": state,
            "position": position,
            "a_count": a_count,
            "c_count": c_count,
            "summary": f"市场状态：{state}，AI均分 {avg}，风险 {risk}，建议仓位 {position}",
        }
