# V9.1 Realtime AutoScan

## 启动电脑端

```bash
python -m streamlit run apps/v91_realtime_autoscan.py
```

## 启动手机端

```bash
python -m streamlit run apps/v91_mobile.py --server.address 0.0.0.0 --server.port 8501
```

## 实时数据路径

优先读取：

```text
data/realtime/quotes_realtime.csv
```

备用：

```text
data/inbox/quotes.csv
data/quotes.csv
```

## 推荐字段

```csv
code,name,price,change_pct,main_inflow,trend,capital,risk,quality,lia
```
