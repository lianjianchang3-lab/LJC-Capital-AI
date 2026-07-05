from pathlib import Path
import pandas as pd

class HoldingManager:
    def __init__(self, path="data/portfolio/holdings.csv"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _normalize_code(self, code):
        return str(code).strip().replace(".0","").zfill(6)

    def load(self):
        if not self.path.exists():
            return pd.DataFrame(columns=["code","name","cost","shares","target_weight"])
        df = pd.read_csv(self.path, dtype={"code": str})
        for c in ["code","name","cost","shares","target_weight"]:
            if c not in df.columns:
                df[c] = 0 if c in ["cost","shares","target_weight"] else ""
        df["code"] = df["code"].apply(self._normalize_code)
        for c in ["cost","shares","target_weight"]:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df

    def save(self, df):
        df = df.copy()
        df["code"] = df["code"].apply(self._normalize_code)
        df.to_csv(self.path, index=False)

    def upsert(self, code, name="", cost=0, shares=0, target_weight=0.1):
        df = self.load()
        code = self._normalize_code(code)
        if not name:
            name = code
        row = {"code":code,"name":name,"cost":float(cost),"shares":float(shares),"target_weight":float(target_weight)}
        if code in set(df["code"]):
            for k,v in row.items():
                df.loc[df["code"] == code, k] = v
        else:
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        self.save(df)
        return df

    def remove(self, code):
        df = self.load()
        code = self._normalize_code(code)
        df = df[df["code"] != code]
        self.save(df)
        return df
