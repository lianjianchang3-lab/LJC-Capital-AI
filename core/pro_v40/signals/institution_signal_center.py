import pandas as pd
from core.pro_v40.engine.unified_ai_engine import UnifiedAIEngine

class InstitutionSignalCenter:
    def __init__(self):
        self.engine = UnifiedAIEngine()

    def signals(self):
        df = self.engine.run()
        if df is None or df.empty:
            return pd.DataFrame()

        df = df.copy()
        df["机构信号"] = "普通"
        df.loc[df["统一建议"]=="A类立即关注", "机构信号"] = "★★★★★ 立即关注"
        df.loc[df["统一建议"]=="B类等待回踩", "机构信号"] = "★★★★ 等待回踩"
        df.loc[df["统一建议"]=="C类回避", "机构信号"] = "★ 禁止介入"

        df["执行动作"] = "观察"
        df.loc[df["统一建议"]=="A类立即关注", "执行动作"] = "买入/加仓候选"
        df.loc[df["统一建议"]=="B类等待回踩", "执行动作"] = "等待低吸"
        df.loc[df["统一建议"]=="C类回避", "执行动作"] = "回避/减仓"

        return df.sort_values("Unified AI Score", ascending=False)
