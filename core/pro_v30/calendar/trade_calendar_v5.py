from datetime import datetime

class TradeCalendarV5:
    def __init__(self):
        from core.pro_v30.signal.signal_center_v5 import SignalCenterV5
        from core.pro_v30.risk.portfolio_risk_v5 import PortfolioRiskV5
        self.signal = SignalCenterV5()
        self.risk = PortfolioRiskV5()

    def plan(self):
        sig = self.signal.signals()
        risk = self.risk.analyze()
        top_buy = []
        avoid = []
        if sig is not None and not sig.empty:
            top_buy = sig[sig["信号"].isin(["买入","小仓试探"])].head(5).to_dict("records")
            avoid = sig[sig["信号"].str.contains("回避", na=False)].head(5).to_dict("records")

        risk_level = risk.get("risk_level", "未知")
        if risk_level == "高":
            mode = "防守，不追高"
            morning = "只观察，不主动加仓"
            afternoon = "若冲高，优先降低风险仓位"
            overnight = "降低隔夜仓位"
        elif risk_level == "中":
            mode = "谨慎进攻"
            morning = "只在第一买点附近小仓试探"
            afternoon = "看资金共振再决定是否加仓"
            overnight = "保留强势股，弱势股不隔夜"
        else:
            mode = "积极观察"
            morning = "重点关注买入信号"
            afternoon = "资金共振增强可适度加仓"
            overnight = "优先保留Alpha高、风险低标的"

        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode,
            "pre_open": "阅读晨报，确认仓位上限和重点股票",
            "morning": morning,
            "midday": "复核资金共振与风险变化",
            "afternoon": afternoon,
            "tail": "尾盘确认是否留仓过夜",
            "overnight": overnight,
            "top_buy": top_buy,
            "avoid": avoid,
            "portfolio_risk": risk.get("summary"),
        }

    def text(self):
        p = self.plan()
        lines = [
            "LJC AI 交易日历",
            "="*28,
            f"时间：{p['time']}",
            f"模式：{p['mode']}",
            f"开盘前：{p['pre_open']}",
            f"上午：{p['morning']}",
            f"中午：{p['midday']}",
            f"下午：{p['afternoon']}",
            f"尾盘：{p['tail']}",
            f"隔夜：{p['overnight']}",
            "",
            f"组合风险：{p['portfolio_risk']}",
            "",
            "今日可关注："
        ]
        for i,x in enumerate(p.get("top_buy", [])[:5],1):
            lines.append(f"{i}. {x.get('code')} {x.get('name')}｜{x.get('信号')}｜强度{x.get('信号强度')}｜仓位{x.get('建议仓位')}")
        lines.append("")
        lines.append("今日回避：")
        for i,x in enumerate(p.get("avoid", [])[:5],1):
            lines.append(f"{i}. {x.get('code')} {x.get('name')}｜{x.get('信号')}｜风险{x.get('综合风险')}")
        return "\n".join(lines)
