from pathlib import Path
from datetime import datetime


class ReportEngine:
    def build_daily_report(self, data, out_dir="reports"):
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        file = path / "daily_report.md"
        wr = data["war_room"]
        lines = [
            "# LJC Capital AI Pro Daily Report",
            f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            f"市场：{wr['market']}",
            f"仓位：{wr['position']}",
            f"主线：{wr['theme']}",
            f"Confidence：{wr['confidence']}",
            "",
            "## Diamond Core",
        ]
        for r in data["diamond"]:
            lines.append(f"- {r['code']} {r['name']}：LIA {r['lia']}，{r['action']}，{r['evidence']}")
        lines.append("")
        lines.append("## Opportunity")
        for r in data["opportunity"]:
            lines.append(f"- {r['code']} {r['name']}：LIA {r['lia']}，{r['action']}，{r['evidence']}")
        file.write_text("\n".join(lines), encoding="utf-8")
        return str(file)
