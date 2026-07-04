# LJC Monday Realtime Ready

## 目标

明天完成部署，周一可用。

## 电脑端

```bash
python -m streamlit run apps/monday_realtime_dashboard.py
```

## 手机端

```bash
python -m streamlit run apps/monday_realtime_mobile.py --server.address 0.0.0.0 --server.port 8501
```

## 快速测试

```bash
scripts/monday_realtime_test.command
```

## 数据优先级

1. AKShare 东方财富实时
2. data/realtime/monday_quotes_cache.csv
3. data/realtime/v105_live_cache.csv
4. data/realtime/v101_quotes_cache.csv
5. data/realtime/quotes_realtime.csv
6. data/inbox/quotes.csv
7. data/quotes.csv
