import pandas as pd

class LCRIExplain:
    def __init__(self):
        from core.professional import LCRIPro
        self.lcri = LCRIPro()

    def dataframe(self):
        df = self.lcri.dataframe()
        if df is None or df.empty: return pd.DataFrame()
        df = df.copy()
        for c in ["V8综合分","LCRI Score","机构共振指数","risk_score","胜率估算","赔率"]:
            if c not in df.columns: df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        df["推荐原因"] = df.apply(self._positive_reasons, axis=1)
        df["风险原因"] = df.apply(self._risk_reasons, axis=1)
        df["解释文本"] = df.apply(self._explain, axis=1)
        return df.sort_values("V8综合分", ascending=False)

    def _positive_reasons(self, r):
        reasons = []
        if r.get("V8综合分",0) >= 80: reasons.append("综合评分较高")
        if r.get("机构共振指数",0) >= 70: reasons.append("机构共振较强")
        if r.get("LCRI Score",0) >= 75: reasons.append("LCRI处于优势区间")
        if r.get("胜率估算",0) >= 70: reasons.append("胜率估算较好")
        return "、".join(reasons) if reasons else "暂未形成强优势"

    def _risk_reasons(self, r):
        risks = []
        if r.get("risk_score",0) < 55: risks.append("风险评分偏弱")
        if r.get("V8综合分",0) < 60: risks.append("综合分不足")
        if r.get("机构共振指数",0) < 45: risks.append("机构共振不足")
        return "、".join(risks) if risks else "风险可控"

    def _explain(self, r):
        return f"{r.get('name')}：{r.get('V8动作','观察')}。综合分{r.get('V8综合分')}，LCRI{r.get('LCRI Score')}，机构共振{r.get('机构共振指数')}，风险{r.get('risk_score')}，胜率{r.get('胜率估算')}%。推荐原因：{r.get('推荐原因')}；风险原因：{r.get('风险原因')}。"
