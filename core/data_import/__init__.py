from pathlib import Path
import pandas as pd
import shutil
from datetime import datetime

class InboxImporter:
    def __init__(self, inbox="data/inbox"):
        self.inbox = Path(inbox)
        self.inbox.mkdir(parents=True, exist_ok=True)
        Path("data/processed").mkdir(parents=True, exist_ok=True)

    def import_all(self):
        results = []
        for p in self.inbox.glob("*.csv"):
            try:
                df = pd.read_csv(p, encoding="utf-8-sig", dtype={"code": str, "代码": str})
            except Exception:
                df = pd.read_csv(p, encoding="gbk", dtype={"code": str, "代码": str})
            cols = set(df.columns)
            if {"超大单", "大单"} & cols or {"super_large", "large"} & cols:
                target = "data/capital.csv"
            elif {"持仓", "成本"} & cols or {"shares", "cost"} & cols:
                target = "data/portfolio.csv"
            else:
                target = "data/quotes.csv"
            df.to_csv(target, index=False, encoding="utf-8-sig")
            shutil.move(str(p), f"data/processed/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{p.name}")
            results.append({"file": p.name, "target": target, "rows": len(df)})
        return results

class TemplateManager:
    def __init__(self, template_dir="data/templates", inbox_dir="data/inbox"):
        self.template_dir = Path(template_dir)
        self.inbox_dir = Path(inbox_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.inbox_dir.mkdir(parents=True, exist_ok=True)

    def list_templates(self):
        return [p.name for p in self.template_dir.glob("*.csv")]

    def copy_template_to_inbox(self, name):
        src = self.template_dir / name
        dst = self.inbox_dir / name
        shutil.copy2(src, dst)
        return {"ok": True, "message": f"已复制 {name} 到 inbox"}
