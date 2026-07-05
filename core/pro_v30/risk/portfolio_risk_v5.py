import pandas as pd

class PortfolioRiskV5:
    def __init__(self):
        from core.pro_v30.portfolio.portfolio_center_v3 import PortfolioCenterV3
        self.portfolio = PortfolioCenterV3()

    def analyze(self):
        p = self.portfolio.analyze()
        df = p.get("table")
        if df is None or len(df)==0:
            return {"status":"NO DATA","summary":"暂无持仓数据","table":pd.DataFrame()}

        df = df.copy()
        for c in ["市值","Alpha2.0","综合风险","资金共振","shares","target_weight"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        total_mv = float(df["市值"].sum())
        stock_count = int((df["shares"]>0).sum())
        avg_alpha = round(float(df["Alpha2.0"].mean()), 1) if len(df)>0 else 0
        avg_risk = round(float(df["综合风险"].mean()), 1) if len(df)>0 else 0
        avg_capital = round(float(df["资金共振"].mean()), 1) if len(df)>0 else 0

        concentration = 0
        if total_mv > 0:
            concentration = round(float((df["市值"]/total_mv).max()*100), 1)

        # 简化组合指标，先可用，后续接入历史净值和行业分类
        portfolio_beta = round(0.8 + avg_risk/200, 2)
        portfolio_alpha = round(avg_alpha - avg_risk*0.25, 1)
        drawdown_est = round(min(35, 8 + avg_risk*0.22 + concentration*0.08), 1)
        sharpe_est = round(max(0, (portfolio_alpha/20) - (drawdown_est/25)), 2)

        risk_level = "低"
        if avg_risk >= 45 or concentration >= 35:
            risk_level = "中"
        if avg_risk >= 70 or concentration >= 55:
            risk_level = "高"

        suggestion = "保持均衡"
        if risk_level == "高":
            suggestion = "降低仓位，减少单票集中"
        elif avg_alpha >= 75 and avg_risk < 45:
            suggestion = "可适度进攻"
        elif avg_alpha < 60:
            suggestion = "以防守为主"

        summary = f"组合Alpha {avg_alpha}，风险 {avg_risk}，集中度 {concentration}%，风险等级 {risk_level}，建议：{suggestion}"

        return {
            "status":"OK",
            "summary":summary,
            "total_market_value":round(total_mv,2),
            "stock_count":stock_count,
            "avg_alpha":avg_alpha,
            "avg_risk":avg_risk,
            "avg_capital":avg_capital,
            "concentration":concentration,
            "beta":portfolio_beta,
            "portfolio_alpha":portfolio_alpha,
            "drawdown_est":drawdown_est,
            "sharpe_est":sharpe_est,
            "risk_level":risk_level,
            "suggestion":suggestion,
            "table":df,
        }
