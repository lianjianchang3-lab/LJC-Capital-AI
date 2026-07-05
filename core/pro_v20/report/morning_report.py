from core.pro_v20.decision.decision_center import ProDecisionCenter
from core.pro_v20.watchlist.watchlist_center import ProWatchlistCenter
from core.pro_v20.portfolio.portfolio_center import ProPortfolioCenter

class ProMorningReport:
    def __init__(self):
        self.decision = ProDecisionCenter()
        self.watchlist = ProWatchlistCenter()
        self.portfolio = ProPortfolioCenter()

    def build(self):
        brief = self.decision.morning_brief()
        watch = self.watchlist.analyze()
        portfolio = self.portfolio.analyze()
        return {
            "brief": brief,
            "watchlist_rows": int(len(watch)) if watch is not None else 0,
            "watchlist_top": watch.head(10).to_dict("records") if watch is not None and not watch.empty else [],
            "portfolio_status": portfolio.get("status"),
            "portfolio_summary": portfolio.get("summary"),
        }

    def text(self):
        r = self.build()
        b = r.get("brief", {})
        top = r.get("watchlist_top", [])
        lines = []
        lines.append("LJC Pro V2.0 今日晨报")
        lines.append("=" * 28)
        lines.append(f"今日策略：{b.get('summary','暂无')}")
        lines.append(f"AI均分：{b.get('market_score','-')}")
        lines.append(f"市场状态：{b.get('market_mode','-')}")
        lines.append(f"建议仓位：{b.get('position','-')}")
        lines.append("")
        lines.append("今日重点：")
        for i, x in enumerate(top[:8], 1):
            lines.append(
                f"{i}. {x.get('code','')} {x.get('name','')} | "
                f"Alpha {x.get('LJC Alpha Score','-')} | "
                f"{x.get('正式建议','观察')} | "
                f"仓位 {x.get('正式仓位','-')}"
            )
        lines.append("")
        lines.append(f"持仓：{r.get('portfolio_summary','暂无')}")
        return "\n".join(lines)

    # 兼容 Sprint2_9 旧调用
    def generate_text(self):
        return self.text()

    def generate(self):
        return self.build()

# 兼容旧代码：from core.pro_v20.report import MorningReport
MorningReport = ProMorningReport
