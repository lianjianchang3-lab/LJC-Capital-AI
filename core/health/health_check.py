from pathlib import Path
import importlib


class HealthCheck:
    def __init__(self):
        self.required_files = [
            "app.py",
            "VERSION",
            "config/settings.yaml",
            "core/data_center/data_center.py",
            "core/capital/capital_engine.py",
            "core/lia/lia_engine.py",
            "core/decision/decision_engine.py",
            "core/portfolio/portfolio_engine.py",
            "core/data_import/inbox_importer.py",
        ]
        self.required_dirs = [
            "data",
            "data/inbox",
            "data/templates",
            "data/processed",
            "logs",
        ]
        self.required_modules = [
            "streamlit",
            "pandas",
            "yaml",
        ]

    def run(self):
        results = []

        for d in self.required_dirs:
            p = Path(d)
            if not p.exists():
                p.mkdir(parents=True, exist_ok=True)
            results.append({
                "item": d,
                "type": "dir",
                "ok": p.exists(),
                "message": "OK" if p.exists() else "missing",
            })

        for f in self.required_files:
            p = Path(f)
            results.append({
                "item": f,
                "type": "file",
                "ok": p.exists(),
                "message": "OK" if p.exists() else "missing",
            })

        for m in self.required_modules:
            try:
                importlib.import_module(m)
                ok, msg = True, "OK"
            except Exception as e:
                ok, msg = False, str(e)
            results.append({
                "item": m,
                "type": "python",
                "ok": ok,
                "message": msg,
            })

        score = int(100 * sum(1 for r in results if r["ok"]) / max(1, len(results)))
        return {
            "score": score,
            "ok": score >= 90,
            "results": results,
        }
