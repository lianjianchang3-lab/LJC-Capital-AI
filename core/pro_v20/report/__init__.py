try:
    from core.pro_v20.report.morning_report import ProMorningReport
except Exception:
    ProMorningReport = None

__all__ = ["ProMorningReport"]
