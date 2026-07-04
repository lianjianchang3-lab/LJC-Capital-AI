# V8.3 Autonomous Investment Engine

## M1 Realtime Data Engine
统一 Provider Manager，目前 CSV fallback，预留实时 Provider。

## M2 Alpha Validation Center
每只股票生成验证卡：为什么买、历史样本、胜率、收益、风险、可信度。

## M3 AI Learning Engine
根据 Alpha Validation 自动生成模型权重建议，并保存模型版本。

## M4 Portfolio AI
根据 Alpha Cards 自动生成目标仓位和现金比例。

## M5 Institution Committee
趋势/资金/量化/风险/组合投票，输出最终建议。

## 启动

```bash
python -m streamlit run apps/v83_autonomous_engine.py
```
