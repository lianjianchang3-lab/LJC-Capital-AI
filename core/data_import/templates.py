from pathlib import Path
import shutil


class TemplateManager:
    def __init__(self, template_dir="data/templates", inbox_dir="data/inbox"):
        self.template_dir = Path(template_dir)
        self.inbox_dir = Path(inbox_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.inbox_dir.mkdir(parents=True, exist_ok=True)

    def list_templates(self):
        return sorted([p.name for p in self.template_dir.glob("*.csv")])

    def copy_template_to_inbox(self, template_name):
        src = self.template_dir / template_name
        if not src.exists():
            return {"ok": False, "message": f"模板不存在：{template_name}"}
        dst = self.inbox_dir / template_name
        shutil.copy2(src, dst)
        return {"ok": True, "message": f"已复制到 inbox：{dst}"}
