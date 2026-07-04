# LJC V9.0 Realtime Test Deploy

## 启动 PC 版

```bash
python -m streamlit run apps/v90_realtime_os.py
```

或双击：

```bash
scripts/start_v90_realtime_os.command
```

## 启动手机端

```bash
python -m streamlit run apps/v90_mobile.py --server.address 0.0.0.0 --server.port 8501
```

或双击：

```bash
scripts/start_v90_mobile.command
```

## 实时数据文件

优先读取：

```text
data/realtime/quotes_realtime.csv
```

备用：

```text
data/inbox/quotes.csv
data/quotes.csv
```

## 字段建议

```csv
code,name,price,change_pct,main_inflow,trend,capital,risk,quality,lia
```
