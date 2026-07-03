# V8.2 Build002 Pure Cloud Realtime

## 目标

手机端 / Streamlit Cloud 直接拉取公开行情快照，不再依赖 Mac 本地脚本更新。

## 新增

- `CloudRealtimeService`
- App 新增「手机实时」页面
- LIA + 实时价格合并展示

## 注意

当前实现的是公开行情快照：

- 最新价
- 涨跌幅
- 成交额
- 行情时间

不是 Level-2 / 逐笔成交 / 实时主力资金。

后续资金实时需要接：

- Moomoo OpenD + 云桥
- 东方财富资金接口
- 付费行情数据
- Supabase / Firebase 云数据库
