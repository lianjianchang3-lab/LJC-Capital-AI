from datetime import datetime
import pandas as pd
import urllib.request


class SinaRealtimeProvider:
    def _market_code(self, code: str) -> str:
        code = str(code).zfill(6)
        if code.startswith(("6", "9")):
            return "sh" + code
        return "sz" + code

    def fetch_quotes(self, codes):
        symbols = ",".join(self._market_code(c) for c in codes)
        url = f"https://hq.sinajs.cn/list={symbols}"
        req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn/"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read().decode("gbk", errors="ignore")

        rows = []
        today = datetime.now().strftime("%Y-%m-%d")
        for line in raw.splitlines():
            if '="' not in line:
                continue
            left, right = line.split('="', 1)
            symbol = left.split("_")[-1]
            code = symbol[-6:]
            values = right.strip('";').split(",")
            if len(values) < 32 or not values[0]:
                continue

            name = values[0]
            open_price = self._num(values[1])
            pre_close = self._num(values[2])
            price = self._num(values[3])
            high = self._num(values[4])
            low = self._num(values[5])
            volume = self._num(values[8])
            amount = self._num(values[9]) / 100000000
            time_text = values[31] if len(values) > 31 else ""

            change_pct = 0.0
            if pre_close:
                change_pct = round((price - pre_close) / pre_close * 100, 2)

            rows.append({
                "date": today,
                "time": time_text,
                "code": code,
                "name": name,
                "close": price,
                "change_pct": change_pct,
                "volume_ratio": 1.0,
                "turnover": round(amount, 2),
                "open": open_price,
                "high": high,
                "low": low,
                "source": "sina_realtime",
            })

        return pd.DataFrame(rows)

    def _num(self, x):
        try:
            return float(x)
        except Exception:
            return 0.0
