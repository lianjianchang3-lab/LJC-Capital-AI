import pandas as pd
from core.decision import DecisionCore
from core.institution import InstitutionEngine

class AITrader:
    def __init__(self):
        self.decision = DecisionCore()
        self.institution = InstitutionEngine()

    def signals(self):
        base = self.decision.trade_plan()
        inst = self.institution.run()
        if base is None or base.empty:
            return pd.DataFrame()
        if inst is None or inst.empty:
            df = base.copy()
        else:
            keep = ["code", "机构共振指数", "机构评级", "机构动作", "机构证据", "北向模拟分", "龙虎榜模拟分", "基金关注分"]
            df = base.merge(inst[keep], on="code", how="left")

        for c in ["price", "LCRI Score", "risk_score", "机构共振指数", "change_pct"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["第一买点"] = (df["price"] * 0.985).round(2)
        df["第二买点"] = (df["price"] * 0.965).round(2)
        df["突破确认价"] = (df["price"] * 1.025).round(2)
        df["止损价"] = (df["price"] * 0.93).round(2)
        df["第一止盈"] = (df["price"] * 1.10).round(2)
        df["第二止盈"] = (df["price"] * 1.20).round(2)

        df["AI交易强度"] = (
            df["LCRI Score"] * 0.45
            + df["机构共振指数"] * 0.35
            + df["risk_score"] * 0.20
        ).round(1)

        df["执行建议"] = "观察"
        df.loc[(df["AI交易强度"] >= 88) & (df["risk_score"] >= 65), "执行建议"] = "买入关注"
        df.loc[(df["AI交易强度"] >= 75) & (df["risk_score"] >= 55), "执行建议"] = "小仓试探"
        df.loc[(df["risk_score"] < 45) | (df["LCRI Score"] < 50), "执行建议"] = "回避/减仓"

        df["建议仓位V5"] = "0%-3%"
        df.loc[df["执行建议"] == "小仓试探", "建议仓位V5"] = "3%-8%"
        df.loc[df["执行建议"] == "买入关注", "建议仓位V5"] = "8%-15%"
        df.loc[df["执行建议"] == "回避/减仓", "建议仓位V5"] = "0%"

        df["执行理由"] = df.apply(
            lambda r: f"LCRI={r['LCRI Score']} 机构={r.get('机构共振指数',0)} 风险={r['risk_score']}｜买点{r['第一买点']}/{r['第二买点']} 止损{r['止损价']}",
            axis=1
        )
        return df.sort_values("AI交易强度", ascending=False)

    def today_plan_text(self):
        df = self.signals()
        if df.empty:
            return "暂无交易信号"
        lines = ["LJC V5.1 AI Trader 今日执行计划", "="*34]
        for i, (_, r) in enumerate(df.head(8).iterrows(), 1):
            lines.append(f"{i}. {r.get('code')} {r.get('name')}｜{r.get('执行建议')}｜强度{r.get('AI交易强度')}｜仓位{r.get('建议仓位V5')}")
            lines.append(f"   买点：{r.get('第一买点')}/{r.get('第二买点')}｜突破：{r.get('突破确认价')}｜止损：{r.get('止损价')}｜目标：{r.get('第一止盈')}/{r.get('第二止盈')}")
            lines.append(f"   理由：{r.get('执行理由')}")
        return "\n".join(lines)
