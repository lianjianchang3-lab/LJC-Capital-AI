class MainForceEngine:
    def summary(self, code, mf_df):
        rows = mf_df[mf_df["code"] == code].sort_values("date")
        if rows.empty:
            return {
                "mf_1d": 0, "mf_3d": 0, "mf_5d": 0,
                "capital_health": 50, "capital_state": "暂无资金数据",
                "latest_date": "-"
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
            "mf_accel": accel,
            "capital_health": score,
            "capital_state": state,
            "latest_date": str(rows.iloc[-1]["date"].date()),
        }
