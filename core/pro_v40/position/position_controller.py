import pandas as pd
from core.pro_v40.engine.unified_ai_engine import UnifiedAIEngine

class PositionController:
    def __init__(self):
        self.engine = UnifiedAIEngine()

    def allocation(self):
        df = self.engine.run()
        state = self.engine.market_state()
        if df.empty:
            return {"status":"NO DATA","summary":"暂无数据","items":[]}

        max_total = state.get("position", "20%-40%")
        rows = []
        for _, r in df.head(20).iterrows():
            score = float(r.get("Unified AI Score",0))
            risk = float(r.get("综合风险",0))
            if r.get("统一建议") == "A类立即关注":
                weight = 0.08 if risk >= 45 else 0.12
            elif r.get("统一建议") == "B类等待回踩":
                weight = 0.03
            else:
                weight = 0.0
            rows.append({
                "code": r.get("code"),
                "name": r.get("name"),
                "统一建议": r.get("统一建议"),
                "AI分数": score,
                "风险": risk,
                "建议个股仓位": f"{round(weight*100)}%",
                "操作": "可执行" if weight>0 else "不参与",
                "证据链": r.get("证据链"),
            })
        summary = f"建议总仓位 {max_total}，A类机会 {state.get('a_count')} 个，回避 {state.get('c_count')} 个"
        return {"status":"OK","summary":summary,"total_position":max_total,"items":rows}
