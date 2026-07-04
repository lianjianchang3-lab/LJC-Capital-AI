# V9.3 Sprint B - AutoSwitch Scanner

## 功能

- 基于 Sprint A RealtimeCore
- AKShare 优先，CSV 备用
- 全市场/本地市场扫描
- AI Score V3
- BUY / WATCH_BUY / RISK_ALERT / AVOID
- 手机端信号卡片

## 启动电脑端

```bash
python -m streamlit run apps/v93_sprint_b_scanner.py
```

## 启动手机端

```bash
python -m streamlit run apps/v93_mobile_scanner.py --server.address 0.0.0.0 --server.port 8501
```
