import pandas as pd


class TradingCockpit:
    """
    V8.5 Build005 主交易驾驶舱。
    统一汇总：
    - EnterpriseCommander 市场状态
    - ExecutionCenter 执行建议
    - PortfolioCenter 持仓
    - WatchlistCenter 自选股
    - DailyPlan 每日计划
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

    def _safe(self, label, fn, default):
        try:
            return fn()
        except Exception as e:
            return default

    def snapshot(self):
        commander = self._safe("commander", lambda: self.commander.snapshot(), {})
        market = commander.get("market", {}) or {}
        radar_health = commander.get("radar_health", {}) or {}

        execution = self._safe("execution", lambda: self.execution.dataframe(), pd.DataFrame())
        portfolio = self._safe("portfolio", lambda: self.portfolio.analyze(), pd.DataFrame())
        portfolio_summary = self._safe("portfolio_summary", lambda: self.portfolio.summary(), {"summary": "暂无持仓", "total_value": 0, "pnl": 0, "risk_count": 0})
        watchlist = self._safe("watchlist", lambda: self.watchlist.analyze(), pd.DataFrame())
        watchlist_summary = self._safe("watchlist_summary", lambda: self.watchlist.summary(), {"summary": "暂无自选股", "focus": 0, "avoid": 0})

        buy = self._filter_buy(execution)
        avoid = self._filter_avoid(execution)
        hold = self._filter_hold(portfolio)
        reduce = self._filter_reduce(portfolio)

        return {
            "market": market,
            "radar_health": radar_health,
            "summary": commander.get("summary") or market.get("summary") or "-",
            "execution": execution,
            "portfolio": portfolio,
            "portfolio_summary": portfolio_summary,
            "watchlist": watchlist,
            "watchlist_summary": watchlist_summary,
            "buy": buy,
            "avoid": avoid,
            "hold": hold,
            "reduce": reduce,
            "plan_text": self.plan_text(market, buy, hold, reduce, avoid, portfolio_summary, watchlist_summary),
        }

    def _filter_buy(self, df):
        if df is None or df.empty:
            return pd.DataFrame()
        if "买入优先级" in df.columns:
            return df[df["买入优先级"].fillna(9) <= 3].head(10)
        return df.head(10)

    def _filter_avoid(self, df):
        if df is None or df.empty:
            return pd.DataFrame()
        if "买入优先级" in df.columns:
            return df[df["买入优先级"].fillna(0) == 9].head(10)
        if "V8动作" in df.columns:
            return df[df["V8动作"].astype(str).str.contains("回避", na=False)].head(10)
        return pd.DataFrame()

    def _filter_hold(self, df):
        if df is None or df.empty:
            return pd.DataFrame()
        if "持仓建议" in df.columns:
            return df[df["持仓建议"].astype(str).str.contains("持有|止盈", na=False)].head(10)
        return df.head(10)

    def _filter_reduce(self, df):
        if df is None or df.empty:
            return pd.DataFrame()
        if "持仓建议" in df.columns:
            return df[df["持仓建议"].astype(str).str.contains("止损|减仓|回避", na=False)].head(10)
        return pd.DataFrame()

    def plan_text(self, market, buy, hold, reduce, avoid, pf_summary, wl_summary):
        lines = ["LJC V8.5 Build005 今日交易驾驶舱", "=" * 36]
        lines.append(f"市场：{market.get('state','-')}｜建议仓位：{market.get('position','-')}｜LCRI均分：{market.get('lcri_avg','-')}")
        lines.append(f"持仓：{pf_summary.get('summary','-')}")
        lines.append(f"自选：{wl_summary.get('summary','-')}")
        lines.append("")
        lines.append("一、今天可以买/重点关注：")
        if buy is None or buy.empty:
            lines.append("- 暂无")
        else:
            for _, r in buy.head(5).iterrows():
                lines.append(f"- {r.get('code')} {r.get('name')}｜优先级{r.get('买入优先级')}｜首仓{r.get('首次建仓')}｜最大{r.get('最大允许仓位')}｜止损{r.get('止损价')}")
        lines.append("")
        lines.append("二、持仓继续观察：")
        if hold is None or hold.empty:
            lines.append("- 暂无")
        else:
            for _, r in hold.head(5).iterrows():
                lines.append(f"- {r.get('code')} {r.get('name')}｜{r.get('持仓建议')}｜盈亏{r.get('浮盈浮亏%')}%｜{r.get('组合操作')}")
        lines.append("")
        lines.append("三、今天减仓/风险：")
        if reduce is None or reduce.empty:
            lines.append("- 暂无")
        else:
            for _, r in reduce.head(5).iterrows():
                lines.append(f"- {r.get('code')} {r.get('name')}｜{r.get('持仓建议')}｜{r.get('组合操作')}")
        lines.append("")
        lines.append("四、今天回避：")
        if avoid is None or avoid.empty:
            lines.append("- 暂无")
        else:
            for _, r in avoid.head(5).iterrows():
                lines.append(f"- {r.get('code')} {r.get('name')}｜{r.get('执行结论') or r.get('V8动作')}")
        return "\n".join(lines)
