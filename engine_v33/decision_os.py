from engine_v33.data_engine import DataEngineV33


class V33DecisionOS:
    def __init__(self):
        self.data = DataEngineV33()

    def _main_force_summary(self, code, mf):
        rows = mf[mf["code"] == code].sort_values("date")
        if rows.empty:
            return {
                "mf_1d": 0, "mf_3d": 0, "mf_5d": 0, "capital_health": 50,
                "capital_state": "暂无资金数据", "latest_date": "-"
            }

        series = rows["main_force"].tolist()
        one = round(series[-1], 2)
        three = round(sum(series[-3:]), 2)
        five = round(sum(series[-5:]), 2)
        accel = round(series[-1] - series[-2], 2) if len(series) >= 2 else 0

        if len(series) >= 5 and all(x > 0 for x in series[-5:]) and accel > 0:
            state, score = "连续吸筹增强", 95
        elif len(series) >= 3 and all(x > 0 for x in series[-3:]):
            state, score = "持续流入", 86
        elif three < 0:
            state, score = "资金转弱", 55
        else:
            state, score = "震荡观察", 70

        return {
            "mf_1d": one,
            "mf_3d": three,
            "mf_5d": five,
            "capital_health": score,
            "capital_state": state,
            "latest_date": str(rows.iloc[-1]["date"].date()),
        }

    def run(self):
        watch = self.data.watchlist()
        mf = self.data.main_force()
        daily = self.data.stock_daily()

        rows = []
        for _, s in watch.iterrows():
            m = self._main_force_summary(s["code"], mf)
            base_lia = float(s.get("base_lia", 80))
            risk = float(s.get("risk", 35))
            lia = round(base_lia * 0.55 + m["capital_health"] * 0.35 + (100 - risk) * 0.10, 1)
            confidence = round(min(98, lia - risk * 0.05), 1)

            if lia >= 90 and m["capital_health"] >= 88 and risk <= 25:
                pool, action, priority = "Diamond Core", "持有/低吸做T", "S"
            elif lia >= 84 and m["capital_health"] >= 78:
                pool, action, priority = "Opportunity", "等待右侧确认", "A"
            else:
                pool, action, priority = "Watch", "持续跟踪", "B"

            if m["capital_state"] == "资金转弱":
                action, priority = "降级观察/不加仓", "C"

            price_row = daily[daily["code"] == s["code"]]
            close = "-" if price_row.empty else price_row.iloc[-1]["close"]
            change_pct = "-" if price_row.empty else price_row.iloc[-1]["change_pct"]

            rows.append({
                "code": s["code"],
                "name": s["name"],
                "theme": s["theme"],
                "risk": risk,
                "lia": lia,
                "confidence": confidence,
                "pool": pool,
                "action": action,
                "priority": priority,
                "close": close,
                "change_pct": change_pct,
                **m,
                "evidence": f"{m['capital_state']}，5日主力合计 {m['mf_5d']} 亿，数据日期 {m['latest_date']}",
            })

        rows = sorted(rows, key=lambda x: (x["priority"] == "S", x["lia"]), reverse=True)
        diamond = [r for r in rows if r["pool"] == "Diamond Core"]
        opportunity = [r for r in rows if r["pool"] == "Opportunity"]
        watch_rows = [r for r in rows if r["pool"] == "Watch"]

        alerts = []
        for r in rows:
            if r["capital_health"] >= 90:
                alerts.append(f"🟢 {r['name']}：主力资金连续增强，Capital Health {r['capital_health']}")
            if r["capital_state"] == "资金转弱":
                alerts.append(f"🔴 {r['name']}：资金转弱，进入降级观察")

        avg_conf = round(sum(r["confidence"] for r in rows) / max(len(rows), 1), 1)
        buy = opportunity[0]["name"] if opportunity else "暂无"
        t = diamond[0]["name"] if diamond else "暂无"

        return {
            "war_room": {
                "market": "机构主线",
                "position": "75%" if avg_conf >= 86 else "60%",
                "theme": "商业航天 / AI基础设施",
                "confidence": avg_conf,
                "mission": f"重点关注 {buy}；做T候选 {t}；资金转弱股票不加仓。",
            },
            "diamond": diamond,
            "opportunity": opportunity,
            "watch": watch_rows,
            "alerts": alerts or ["暂无重大预警"],
            "rows": rows,
        }
