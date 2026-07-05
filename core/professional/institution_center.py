import pandas as pd

class InstitutionCenter:
    def __init__(self):
        try:
            from core.institution import InstitutionEngine
            self.engine = InstitutionEngine()
        except Exception:
            self.engine = None

    def dataframe(self):
        if self.engine is None:
            return pd.DataFrame()
        try:
            df = self.engine.run()
        except Exception:
            return pd.DataFrame()
        if df is None or df.empty:
            return pd.DataFrame()

        df = df.copy()
        for c in ["机构共振指数", "北向模拟分", "龙虎榜模拟分", "基金关注分", "机构成交强度", "LCRI Score"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["V8机构热度"] = (df["机构共振指数"] * 0.45 + df["北向模拟分"] * 0.20 + df["龙虎榜模拟分"] * 0.20 + df["基金关注分"] * 0.15).round(1)
        df["资金状态"] = "平衡"
        df.loc[df["V8机构热度"] >= 75, "资金状态"] = "资金增强"
        df.loc[df["V8机构热度"] >= 88, "资金状态"] = "强共振"
        df.loc[df["V8机构热度"] < 45, "资金状态"] = "资金偏弱"
        return df.sort_values("V8机构热度", ascending=False)

    def summary(self):
        df = self.dataframe()
        if df.empty:
            return {"status": "NO DATA", "summary": "暂无机构数据"}
        names = "、".join([str(x) for x in df.head(3).get("name", [])])
        avg = round(float(df["V8机构热度"].mean()), 1)
        return {"status": "OK", "avg_heat": avg, "top_names": names, "summary": f"机构平均热度 {avg}，当前重点：{names}"}
