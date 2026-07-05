try:
    from core.pro_v20.config.config_center import ProConfigCenter
except Exception:
    ProConfigCenter = None

__all__ = ["ProConfigCenter"]
