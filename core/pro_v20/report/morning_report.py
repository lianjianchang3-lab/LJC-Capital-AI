from datetime import datetime
from pathlib import Path
import pandas as pd
from core.pro_v20.decision import ProDecisionCenter
from core.pro_v20.trading import TradePlanEngine
from core.pro_v20.scanner import MarketScanner
from core.pro_v20.alerts import AlertCenter

class MorningReport:
    def generate_text(self):
        brief = ProDecisionCenter().morning_brief()
        plans = TradePlanEngine().plans().head(8)
        sectors = MarketScanner().hot_sectors().head(5)
        alerts = AlertCenter().generate()

        lines = []
        lines.append(f"# LJC Pro V2.0 今日作战计划")
        lines.append(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append(f"市场状态：{brief.get('market_mode')}")
        lines.append(f"AI均分：{brief.get('market_score')}")
        lines.append(f"建议仓位：{brief.get('position')}")
        lines.append(f"摘要：{brief.get('summary')}")
        lines.append("")
        lines.append("## 今日重点")
        for _, r in plans.iterrows():
            lines.append(f"- {r.get('红绿灯','')} {r.get('code')} {r.get('name')} | Alpha {r.get('LJC Alpha Score')} | {r.get('交易动作')} | 仓位 {r.get('正式仓位')}")
        lines.append("")
        lines.append("## 热点板块")
        if not sectors.empty:
            for _, r in sectors.iterrows():
                lines.append(f"- {r.get('sector')} | Alpha {r.get('平均Alpha')} | 涨幅 {r.get('平均涨幅')}%")
        lines.append("")
        lines.append("## 预警")
        for a in alerts[:10]:
            lines.append(f"- {a['level']} {a['code']} {a['name']}：{a['alert']}，{a['reason']}")

        text = "\n".join(lines)
        Path("data/reports").mkdir(parents=True, exist_ok=True)
        Path("data/reports/morning_report.md").write_text(text, encoding="utf-8")
        return text
