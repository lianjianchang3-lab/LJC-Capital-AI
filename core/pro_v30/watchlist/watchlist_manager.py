from pathlib import Path
import pandas as pd

class WatchlistManager:
    def __init__(self, path="config/ljc_watchlist.csv"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _normalize_code(self, code):
        code = str(code).strip().replace(".0", "")
        return code.zfill(6)

    def load(self):
        if not self.path.exists():
            return pd.DataFrame(columns=["code","name","group","enabled","star","sort"])
        df = pd.read_csv(self.path, dtype={"code": str})
        for c in ["code","name","group","enabled","star","sort"]:
            if c not in df.columns:
                df[c] = "" if c in ["code","name","group"] else 1
        df["code"] = df["code"].apply(self._normalize_code)
        df["enabled"] = pd.to_numeric(df["enabled"], errors="coerce").fillna(1).astype(int)
        df["star"] = pd.to_numeric(df["star"], errors="coerce").fillna(1).astype(int)
        df["sort"] = pd.to_numeric(df["sort"], errors="coerce").fillna(999).astype(int)
        return df.sort_values(["sort","code"])

    def save(self, df):
        df = df.copy()
        df["code"] = df["code"].apply(self._normalize_code)
        df.to_csv(self.path, index=False)

    def add(self, code, name="", group="未分组", star=1):
        df = self.load()
        code = self._normalize_code(code)
        if not name:
            name = self.guess_name(code)
        if code in set(df["code"]):
            df.loc[df["code"] == code, ["name","group","enabled","star"]] = [name, group, 1, star]
        else:
            sort = int(df["sort"].max()+1) if len(df) else 1
            df = pd.concat([df, pd.DataFrame([{
                "code": code, "name": name, "group": group, "enabled": 1, "star": star, "sort": sort
            }])], ignore_index=True)
        self.save(df)
        return df

    def remove(self, code):
        df = self.load()
        code = self._normalize_code(code)
        df = df[df["code"] != code]
        self.save(df)
        return df

    def enable(self, code, enabled=1):
        df = self.load()
        code = self._normalize_code(code)
        df.loc[df["code"] == code, "enabled"] = int(enabled)
        self.save(df)
        return df

    def enabled_codes(self):
        df = self.load()
        return df[df["enabled"] == 1]["code"].tolist()

    def guess_name(self, code):
        name_map = {
            "300059":"东方财富","688387":"信科移动","688008":"澜起科技",
            "300762":"上海瀚讯","300136":"信维通信","603308":"应流股份",
            "300342":"天银机电","688568":"中科星图","601698":"中国卫通",
            "600879":"航天电子","002463":"沪电股份","300308":"中际旭创",
            "688256":"寒武纪","002371":"北方华创","300502":"新易盛"
        }
        return name_map.get(self._normalize_code(code), "待识别")
