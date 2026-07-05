class CommanderProV5:
    def __init__(self):
        from core.pro_v30.signal.signal_center_v5 import SignalCenterV5
        from core.pro_v30.risk.portfolio_risk_v5 import PortfolioRiskV5
        from core.pro_v30.calendar.trade_calendar_v5 import TradeCalendarV5
        self.signal = SignalCenterV5()
        self.risk = PortfolioRiskV5()
        self.calendar = TradeCalendarV5()

    def dashboard(self):
        sig = self.signal.signals()
        risk = self.risk.analyze()
        cal = self.calendar.plan()
        top = sig.head(10).to_dict("records") if sig is not None and not sig.empty else []
        buy_count = int(sig["信号"].isin(["买入","小仓试探"]).sum()) if sig is not None and not sig.empty else 0
        return {
            "status":"OK" if top else "NO DATA",
            "mode": cal.get("mode"),
            "risk_level": risk.get("risk_level"),
            "risk_summary": risk.get("summary"),
            "portfolio_alpha": risk.get("portfolio_alpha"),
            "drawdown_est": risk.get("drawdown_est"),
            "sharpe_est": risk.get("sharpe_est"),
            "buy_count": buy_count,
            "top": top,
            "calendar": cal,
        }
