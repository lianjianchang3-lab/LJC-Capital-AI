import pandas as pd

class ExecutionCenter:
    def __init__(self):
        from core.professional import LCRIPro
        self.lcri = LCRIPro()

    def dataframe(self):
        df = self.lcri.dataframe()
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        for c in ["V8综合分","risk_score","胜率估算","赔率","机构共振指数","LCRI Score"]:
            if c not in df.columns: df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["买入优先级"] = 5
        df.loc[df["V8综合分"] >= 70, "买入优先级"] = 4
        df.loc[df["V8综合分"] >= 80, "买入优先级"] = 3
        df.loc[df["V8综合分"] >= 88, "买入优先级"] = 2
        df.loc[(df["V8综合分"] >= 92) & (df["risk_score"] >= 75), "买入优先级"] = 1
        if "V8动作" in df.columns:
            df.loc[df["V8动作"].astype(str).str.contains("回避", na=False), "买入优先级"] = 9

        df["首次建仓"] = "0%-3%"
        df.loc[df["买入优先级"] <= 4, "首次建仓"] = "3%-5%"
        df.loc[df["买入优先级"] <= 3, "首次建仓"] = "5%-8%"
        df.loc[df["买入优先级"] <= 2, "首次建仓"] = "8%-12%"
        df.loc[df["买入优先级"] == 1, "首次建仓"] = "10%-15%"
        df.loc[df["买入优先级"] == 9, "首次建仓"] = "0%"

        df["最大允许仓位"] = "5%"
        df.loc[df["买入优先级"] <= 4, "最大允许仓位"] = "8%"
        df.loc[df["买入优先级"] <= 3, "最大允许仓位"] = "12%"
        df.loc[df["买入优先级"] <= 2, "最大允许仓位"] = "15%"
        df.loc[df["买入优先级"] == 1, "最大允许仓位"] = "18%"
        df.loc[df["买入优先级"] == 9, "最大允许仓位"] = "0%"

        df["加仓条件"] = "观察，不主动加仓"
        df.loc[df["买入优先级"] <= 4, "加仓条件"] = "回踩第一买点企稳后加仓"
        df.loc[df["买入优先级"] <= 2, "加仓条件"] = "突破确认价且资金增强后加仓"
        df["减仓条件"] = "跌破止损或评分下降减仓"
        df.loc[df["risk_score"] < 55, "减仓条件"] = "风险偏高，反弹优先减仓"
        df["风险预算"] = "低"
        df.loc[df["risk_score"] < 75, "风险预算"] = "中"
        df.loc[df["risk_score"] < 55, "风险预算"] = "高"
        df["建议持有天数"] = "1-3天"
        df.loc[df["V8综合分"] >= 75, "建议持有天数"] = "3-5天"
        df.loc[df["V8综合分"] >= 85, "建议持有天数"] = "5-10天"
        df.loc[df["V8综合分"] >= 92, "建议持有天数"] = "10天以上跟踪"
        df["执行结论"] = df.apply(self._conclusion, axis=1)
        return df.sort_values(["买入优先级","V8综合分"], ascending=[True,False])

    def _conclusion(self, r):
        if r.get("买入优先级") == 9:
            return f"{r.get('name')}：回避/减仓，风险预算{r.get('风险预算')}，等待评分修复。"
        return f"{r.get('name')}：{r.get('V8动作','观察')}，优先级{r.get('买入优先级')}，首仓{r.get('首次建仓')}，最大{r.get('最大允许仓位')}，止损{r.get('止损价')}，目标{r.get('第一止盈')}/{r.get('第二止盈')}。"

    def text(self, limit=10):
        df = self.dataframe()
        if df.empty: return "暂无 V8.5 执行计划"
        lines = ["LJC V8.5 AI 执行中心", "="*28]
        for i, (_, r) in enumerate(df.head(limit).iterrows(), 1):
            lines.append(f"{i}. {r.get('code')} {r.get('执行结论')}")
            lines.append(f"   买点：{r.get('第一买点')}/{r.get('第二买点')}｜突破：{r.get('突破确认价')}｜加仓：{r.get('加仓条件')}")
        return "\n".join(lines)
