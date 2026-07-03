# V8.2 Build001 Public Realtime Connector

## 新增

- 新浪公开行情快照连接器
- 实时更新 `data/quotes.csv`
- 侧边栏「实时拉取行情」按钮
- 脚本：
  - `update_realtime_quotes.command`
  - `start_realtime_quotes.command`

## 说明

当前版本实现公开行情快照，不是Level-2逐笔资金。
资金数据仍通过 CSV / 后续 Moomoo / 东方财富资金接口接入。
