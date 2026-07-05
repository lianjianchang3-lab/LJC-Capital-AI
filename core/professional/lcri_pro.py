import pandas as pd

class LCRIPro:
    def __init__(self):
        from core.enterprise import EnterpriseCommander
        self.commander = EnterpriseCommander()

    def dataframe(self):
        snap = self.commander.snapshot()
        trader = pd.DataFrame(snap.get("trader_top", []) or [])
        lcri = pd.DataFrame(snap.get("lcri_top", []) or [])
        inst = pd.DataFrame(snap.get("institution_top", []) or [])

        df = trader.copy() if not trader.empty else lcri.copy()
        if df.empty:
            return pd.DataFrame()

        if "code" in df.columns and not inst.empty and "code" in inst.columns:
            keep = [c for c in ["code", "机构共振指数", "机构评级", "机构动作", "机构证据"] if c in inst.columns]
            if keep:
                df = df.merge(inst[keep].drop_duplicates("code"), on="code", how="left")

        for c in ["price", "LCRI Score", "AI交易强度", "risk_score", "机构共振指数", "change_pct"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        ai = df["AI交易强度"]
        df["V8综合分"] = ai.where(ai > 0, df["LCRI Score"] * 0.65 + df["机构共振指数"] * 0.35).round(1)
        df["胜率估算"] = (45 + df["V8综合分"] * 0.42 - (100 - df["risk_score"]) * 0.12).clip(35, 88).round(1)
        df["赔率"] = (1.2 + df["V8综合分"] / 100 * 1.8).round(2)

        defaults = {
            "第一买点": df["price"] * 0.985,
            "第二买点": df["price"] * 0.965,
            "突破确认价": df["price"] * 1.025,
            "止损价": df["price"] * 0.93,
            "第一止盈": df["price"] * 1.10,
            "第二止盈": df["price"] * 1.20,
        }
        for c, v in defaults.items():
            if c not in df.columns:
                df[c] = v.round(2)

        df["风险等级"] = "中"
        df.loc[df["risk_score"] >= 75, "风险等级"] = "低"
        df.loc[df["risk_score"] < 55, "风险等级"] = "高"

        df["V8动作"] = "观察"
        df.loc[(df["V8综合分"] >= 82) & (df["risk_score"] >= 60), "V8动作"] = "重点关注"
        df.loc[(df["V8综合分"] >= 88) & (df["risk_score"] >= 70), "V8动作"] = "强势关注"
        df.loc[(df["V8综合分"] < 55) | (df["risk_score"] < 45), "V8动作"] = "回避"

        df["V8仓位"] = "0%-3%"
        df.loc[df["V8动作"] == "重点关注", "V8仓位"] = "3%-8%"
        df.loc[df["V8动作"] == "强势关注", "V8仓位"] = "8%-15%"
        df.loc[df["V8动作"] == "回避", "V8仓位"] = "0%"

        df["V8理由"] = df.apply(lambda r: f"LCRI={r.get('LCRI Score',0)}｜综合={r.get('V8综合分',0)}｜机构={r.get('机构共振指数',0)}｜风险={r.get('risk_score',0)}｜胜率={r.get('胜率估算',0)}%", axis=1)
        return df.sort_values("V8综合分", ascending=False)

    def execution_text(self, limit=10):
        df = self.dataframe()
        if df.empty:
            return "暂无 V8 执行计划"
        lines = ["LJC V8 今日执行计划", "=" * 26]
        for i, (_, r) in enumerate(df.head(limit).iterrows(), 1):
            lines.append(f"{i}. {r.get('code')} {r.get('name')}｜{r.get('V8动作')}｜综合{r.get('V8综合分')}｜仓位{r.get('V8仓位')}")
            lines.append(f"   买点 {r.get('第一买点')}/{r.get('第二买点')}｜突破 {r.get('突破确认价')}｜止损 {r.get('止损价')}｜目标 {r.get('第一止盈')}/{r.get('第二止盈')}")
            lines.append(f"   {r.get('V8理由')}")
        return "\n".join(lines)
