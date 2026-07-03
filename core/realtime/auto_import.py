from pathlib import Path
from core.data_import import InboxImporter


class AutoImportWatcher:
    def __init__(self, inbox="data/inbox"):
        self.inbox = Path(inbox)
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.importer = InboxImporter(inbox=str(self.inbox))

    def pending_files(self):
        return sorted([p.name for p in self.inbox.glob("*.csv")])

    def has_pending(self):
        return len(self.pending_files()) > 0

    def import_if_pending(self):
        if not self.has_pending():
            return {
                "imported": False,
                "message": "没有待导入CSV。",
                "files": [],
                "results": [],
            }
        results = self.importer.import_all()
        return {
            "imported": True,
            "message": "已自动导入CSV。",
            "files": self.pending_files(),
            "results": results,
        }
