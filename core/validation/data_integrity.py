import pandas as pd
from core.provider import MarketDataProvider


class DataIntegrityValidator:
    def __init__(self, provider=None):
        self.provider = provider or MarketDataProvider()

    def _find_col(self, df, candidates):
        for c in candidates:
            if c in df.columns:
                return c
        return None

    def _numeric_ok(self, df, col):
        if not col or df.empty:
            return False
        converted = pd.to_numeric(df[col], errors="coerce")
        return converted.notna().any()

    def _check(self, condition, item, message):
        return {
            "item": item,
            "pass": bool(condition),
            "status": "PASS" if condition else "FAILED",
            "message": message,
        }

    def validate(self):
        data = self.provider.all()
        quotes = data["quotes"]
        capital = data["capital"]
        portfolio = data["portfolio"]

        checks = []

        checks.append(self._check(not quotes.empty, "quotes.csv", "行情文件存在且可读取"))
        checks.append(self._check("code" in quotes.columns, "quotes.code", "行情存在统一 code 字段"))

        price_col = self._find_col(quotes, ["close", "最新价", "现价", "price", "实时价"])
        chg_col = self._find_col(quotes, ["change_pct", "涨跌幅", "涨幅"])

        checks.append(self._check(price_col is not None, "quotes.price", "行情存在价格字段"))
        checks.append(self._check(self._numeric_ok(quotes, price_col), "quotes.price.numeric", "价格字段可转为数字"))
        checks.append(self._check(chg_col is not None, "quotes.change_pct", "行情存在涨跌幅字段"))

        if "code" in quotes.columns:
            duplicate_count = int(quotes["code"].duplicated().sum())
            checks.append(self._check(duplicate_count == 0, "quotes.duplicates", f"行情代码无重复；重复数={duplicate_count}"))

        checks.append(self._check(not capital.empty, "capital.csv", "资金文件存在且可读取"))
        if not capital.empty:
            checks.append(self._check("code" in capital.columns, "capital.code", "资金存在统一 code 字段"))
            main_col = self._find_col(capital, ["net_main", "主力净流入", "主力净额", "main_inflow"])
            checks.append(self._check(main_col is not None, "capital.main", "资金存在主力净流入字段"))

            if "code" in capital.columns and "code" in quotes.columns:
                q_codes = set(quotes["code"].astype(str))
                c_codes = set(capital["code"].astype(str))
                missing = sorted(list(c_codes - q_codes))[:10]
                checks.append(self._check(len(missing) == 0, "capital.quote_match", f"资金代码均能匹配行情；未匹配={missing}"))

        if not portfolio.empty:
            checks.append(self._check("code" in portfolio.columns, "portfolio.code", "持仓存在统一 code 字段"))
            if "code" in portfolio.columns and "code" in quotes.columns:
                q_codes = set(quotes["code"].astype(str))
                p_codes = set(portfolio["code"].astype(str))
                missing = sorted(list(p_codes - q_codes))[:10]
                checks.append(self._check(len(missing) == 0, "portfolio.quote_match", f"持仓代码均能匹配行情；未匹配={missing}"))
        else:
            checks.append(self._check(True, "portfolio.optional", "持仓文件可为空，不阻塞发布"))

        passed = all(c["pass"] for c in checks)
        return {
            "pass": passed,
            "checks": checks,
            "summary": "PASS" if passed else "FAILED",
        }
