from datetime import datetime
from core.v11.data.data_center import DataCenterV11
from core.v11.market.market_center import MarketCenterV11
from core.v11.ai.ai_center import AICenterV11
from core.v11.portfolio.portfolio_center import PortfolioCenterV11
from core.v11.risk.risk_center import RiskCenterV11

class ReportCenterV11:
    def markdown(self):
        h = DataCenterV11().health(); m = MarketCenterV11().snapshot(); ai = AICenterV11().decisions(); p = PortfolioCenterV11().plan(); r = RiskCenterV11().assess()
        lines = ["# LJC Capital AI V11 RC 日报", f"- 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"- 数据源：{h.get('active_source')} / 行数：{h.get('rows')}", f"- 市场：{m.get('summary')}", f"- AI：{ai.get('summary')}", f"- 组合：{p.get('summary')}", f"- 风险：{r.get('summary')}", "", "## 重点标的"]
        for x in ai.get("items", [])[:8]:
            lines.append(f"- {x.get('code')} {x.get('name')}：{x.get('AI决策')} / {x.get('建议仓位')} / 分数 {x.get('AI综合分')}")
        return "\n".join(lines)
