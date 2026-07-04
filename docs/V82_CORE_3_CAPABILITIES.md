# V8.2 Core 3 Capabilities

## 1. Realtime Provider

文件：
- `core/realtime/realtime_provider.py`
- `data/realtime/quotes_realtime.csv`

当前使用 CSV Adapter，后续可接入 AkShare、Tushare、券商、WebSocket。

## 2. Model Calibration

文件：
- `core/calibration/model_calibrator.py`
- `data/calibration/history_returns.csv`

需要字段：

```csv
code,future_return_5d,future_return_20d
```

用于验证 Investment Score 与未来收益的相关性。

## 3. Signal Backtest

文件：
- `core/backtest_v2/signal_backtester.py`
- `data/backtest/signals_history.csv`

需要字段：

```csv
date,code,signal,entry_price,exit_price
```

用于计算胜率、平均收益、最大单笔亏损。

## 启动

```bash
python -m streamlit run apps/v82_core_lab.py
```
