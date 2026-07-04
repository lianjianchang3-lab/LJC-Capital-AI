from core.intelligence import InstitutionIntelligenceCore

class SignalEngine:
    def __init__(self, core=None):
        self.core = core or InstitutionIntelligenceCore()

    def signals(self):
        df = self.core.score()
        if df.empty:
            return df
        actions = []
        for _, r in df.iterrows():
            if r["lia"] >= 88 and r["risk"] <= 65:
                signal, action = "BUY/HOLD", "核心持有，回调低吸"
            elif r["lia"] >= 80:
                signal, action = "WATCH_BUY", "等待确认，小仓试探"
            elif r["lia"] >= 70:
                signal, action = "WATCH", "观察，不追高"
            elif r["risk"] >= 75:
                signal, action = "REDUCE", "风险偏高，减仓"
            else:
                signal, action = "AVOID", "暂不参与"
            actions.append({"signal": signal, "action": action, "trigger": f"LIA={r['lia']} Risk={r['risk']} Capital={r['capital']}"})
        out = df.copy()
        out["signal"] = [a["signal"] for a in actions]
        out["action"] = [a["action"] for a in actions]
        out["trigger"] = [a["trigger"] for a in actions]
        return out
