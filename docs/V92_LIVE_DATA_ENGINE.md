# LJC V9.2 Live Data Engine

## 目标

完成真实行情接口框架，优先支持 AKShare，失败时自动降级到 CSV。

## 启动电脑端

```bash
python -m streamlit run apps/v92_live_data_engine.py
```

## 启动手机端

```bash
python -m streamlit run apps/v92_mobile.py --server.address 0.0.0.0 --server.port 8501
```

## 安装 AKShare（可选）

```bash
python -m pip install akshare
```

或双击：

```bash
scripts/install_akshare_optional.command
```

## 数据优先级

1. AKShare EastMoney
2. data/realtime/quotes_realtime.csv
3. data/inbox/quotes.csv
4. data/quotes.csv
