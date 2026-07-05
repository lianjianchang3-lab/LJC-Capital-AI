import pandas as pd


class DailyPlan:
    """
    V8.5 Build002 每日交易计划。
    合并市场状态、执行中心、自选股和持仓中心。
    """

    def __init__(self):
        from core.enterprise import EnterpriseCommander
        from core.execution import ExecutionCenter
        from core.portfolio_center import PortfolioCenter
        from core.watchlist_center import WatchlistCenter

        self.commander = EnterpriseCommander()
        self.execution = ExecutionCenter()
        self.portfolio = PortfolioCenter()
        self.watchlist = WatchlistCenter()

    def generate(self):
        snap = self.commander.snapshot()
        market = snap.get("market", {}) or {}
        exe = self.execution.dataframe()
        pf = self.portfolio.analyze()
        wl = self.watchlist.analyze()

        buy = exe[exe["买入优先级"] <= 3].head(5) if exe is not None and not exe.empty else pd.DataFrame()
        avoid = exe[exe["买入优先级"] == 9].head(5) if exe is not None and not exe.empty else pd.DataFrame()
        reduce = pf[pf["持仓建议"].astype(str).str.contains("止损|减仓|回避", na=False)].head(5) if pf is not None and not pf.empty else pd.DataFrame()

        return {
            "market": market,
            "position": market.get("position", "-"),
            "buy": buy.to_dict("records"),
            "avoid": avoid.to_dict("records"),
            "reduce": reduce.to_dict("records"),
            "portfolio_summary": self.portfolio.summary(),
            "watchlist_summary": self.watchlist.summary(),
            "text": self.text(market, buy, reduce, avoid),
        }

    def text(self, market, buy, reduce, avoid):
        lines = ["LJC V8.5 每日交易计划", "=" * 28]
        lines.append(f"市场：{market.get('state','-')}｜建议仓位：{market.get('position','-')}｜LCRI均分：{market.get('lcri_avg','-')}")
        lines.append("")
        lines.append("今日买入/关注：")
        if buy is None or buy.empty:
            lines.append("- 暂无")
        else:
            for _, r in buy.iterrows():
                lines.append(f"- {r.get('code')} {r.get('name')}｜优先级{r.get('买入优先级')}｜首仓{r.get('首次建仓')}｜最大{r.get('最大允许仓位')}")
        lines.append("")
        lines.append("今日减仓/风险：")
        if reduce is None or reduce.empty:
            lines.append("- 暂无")
        else:
            for _, r in reduce.iterrows():
                lines.append(f"- {r.get('code')} {r.get('name')}｜{r.get('持仓建议')}｜{r.get('组合操作')}")
        lines.append("")
        lines.append("今日回避：")
        if avoid is None or avoid.empty:
            lines.append("- 暂无")
        else:
            for _, r in avoid.iterrows():
                lines.append(f"- {r.get('code')} {r.get('name')}｜{r.get('执行结论')}")
        return "\n".join(lines)
