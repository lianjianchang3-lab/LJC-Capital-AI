from datetime import datetime
import pandas as pd

class MorningBriefPro:
    def __init__(self):
        from core.pro_v20.commander import CommanderCenterV2
        from core.pro_v30.portfolio.portfolio_center_v3 import PortfolioCenterV3
        self.commander = CommanderCenterV2()
        self.portfolio = PortfolioCenterV3()

    def build(self):
        d = self.commander.dashboard()
        p = self.portfolio.analyze()
        top = d.get("top", [])[:8]
        return {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "alpha": d.get("alpha"),
            "risk": d.get("risk"),
            "mode": d.get("mode"),
            "position": d.get("position"),
            "summary": d.get("summary"),
            "portfolio": p.get("summary"),
            "top": top,
            "alerts": d.get("alerts", []),
        }

    def text(self):
        b = self.build()
        lines = [
            "LJC Morning Brief Pro",
            "="*30,
            f"时间：{b['date']}",
            f"市场模式：{b.get('mode')}",
            f"Alpha：{b.get('alpha')}｜风险：{b.get('risk')}",
            f"建议仓位：{b.get('position')}",
            f"总结：{b.get('summary')}",
            "",
            "今日重点："
        ]
        for i, x in enumerate(b.get("top", []), 1):
            lines.append(f"{i}. {x.get('code')} {x.get('name')}｜{x.get('最终动作')}｜Alpha {x.get('Alpha2.0')}｜资金 {x.get('资金共振')}｜仓位 {x.get('建议仓位')}")
        lines += ["", f"持仓：{b.get('portfolio')}", "", "预警："]
        alerts = b.get("alerts", [])
        if alerts:
            for a in alerts[:8]:
                lines.append(f"- {a.get('level')} {a.get('code')} {a.get('name')}：{a.get('alert')}")
        else:
            lines.append("- 暂无")
        return "\n".join(lines)
