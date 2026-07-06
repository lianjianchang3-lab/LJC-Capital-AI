from pathlib import Path
import pandas as pd
from core.mobile_ready.offline_cache import OfflineCache


class MobileCommander:
    """
    V8.5 Build006 手机稳定指挥官。
    原则：
    1. 绝不主动全市场拉 AkShare。
    2. 优先读取本地 Execution / Watchlist / Portfolio。
    3. 任一模块失败时降级为缓存或空表，保证手机页面能打开。
    """

    def __init__(self):
        self.cache = OfflineCache()

    def _safe(self, label, fn, default):
        try:
            return fn(), "实时"
        except Exception as e:
            return default, f"降级：{label} {e}"

    def snapshot(self):
        market, market_status = self._safe("market", self._market, {
            "state": "待确认",
            "position": "20%-40%",
            "lcri_avg": "-",
            "summary": "离线模式：等待数据源恢复"
        })

        execution, exe_status = self._safe("execution", self._execution, pd.DataFrame())
        watchlist, wl_status = self._safe("watchlist", self._watchlist, pd.DataFrame())
        portfolio, pf_status = self._safe("portfolio", self._portfolio, pd.DataFrame())

        if isinstance(execution, pd.DataFrame) and not execution.empty:
            self.cache.write_csv("last_execution.csv", execution)
        else:
            execution = self.cache.read_csv("last_execution.csv", pd.DataFrame())

        if isinstance(watchlist, pd.DataFrame) and not watchlist.empty:
            self.cache.write_csv("last_watchlist.csv", watchlist)
        else:
            watchlist = self.cache.read_csv("last_watchlist.csv", pd.DataFrame())

        buy = self._buy(execution)
        risk = self._risk(execution, portfolio)

        return {
            "market": market,
            "execution": execution,
            "watchlist": watchlist,
            "portfolio": portfolio,
            "buy": buy,
            "risk": risk,
            "status": {
                "market": market_status,
                "execution": exe_status,
                "watchlist": wl_status,
                "portfolio": pf_status,
                "cache": self.cache.status(),
            },
            "summary": self._summary(market, buy, risk, watchlist),
        }

    def _market(self):
        from core.enterprise import EnterpriseCommander
        snap = EnterpriseCommander().snapshot()
        m = snap.get("market", {}) or {}
        if not m:
            m = {"state": "待确认", "position": "20%-40%", "lcri_avg": "-", "summary": "无市场数据"}
        return m

    def _execution(self):
        from core.execution import ExecutionCenter
        df = ExecutionCenter().dataframe()
        return df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)

    def _watchlist(self):
        from core.watchlist_center import WatchlistCenter
        df = WatchlistCenter().analyze()
        return df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)

    def _portfolio(self):
        from core.portfolio_center import PortfolioCenter
        df = PortfolioCenter().analyze()
        return df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)

    def _buy(self, df):
        if df is None or df.empty:
            return pd.DataFrame()
        out = df.copy()
        if "买入优先级" in out.columns:
            out["买入优先级"] = pd.to_numeric(out["买入优先级"], errors="coerce").fillna(9)
            return out[out["买入优先级"] <= 3].head(10)
        return out.head(10)

    def _risk(self, exe, pf):
        frames = []
        if pf is not None and not pf.empty and "持仓建议" in pf.columns:
            frames.append(pf[pf["持仓建议"].astype(str).str.contains("止损|减仓|回避", na=False)])
        if exe is not None and not exe.empty:
            if "买入优先级" in exe.columns:
                e = exe.copy()
                e["买入优先级"] = pd.to_numeric(e["买入优先级"], errors="coerce").fillna(0)
                frames.append(e[e["买入优先级"] == 9])
            elif "V8动作" in exe.columns:
                frames.append(exe[exe["V8动作"].astype(str).str.contains("回避", na=False)])
        frames = [x for x in frames if x is not None and not x.empty]
        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True).head(10)

    def _summary(self, market, buy, risk, watchlist):
        return f"市场{market.get('state','-')}，建议仓位{market.get('position','-')}；今日机会{0 if buy is None else len(buy)}只，风险{0 if risk is None else len(risk)}只，自选{0 if watchlist is None else len(watchlist)}只。"
