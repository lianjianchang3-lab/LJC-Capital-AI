# LJC V8.3 Final Test + Mobile Deploy

## Final Acceptance

```bash
python -m streamlit run apps/v83_final_acceptance.py
```

或双击：

```bash
scripts/start_v83_final_acceptance.command
```

## Mobile Deploy

```bash
python -m streamlit run apps/v83_mobile.py --server.address 0.0.0.0 --server.port 8501
```

或双击：

```bash
scripts/start_v83_mobile.command
```

## 手机访问

电脑和手机同一网络：

```bash
ipconfig getifaddr en0
```

手机 Safari 打开：

```text
http://你的Mac_IP:8501
```

## 注意

当前系统是投资研究辅助，不构成自动实盘交易指令。
