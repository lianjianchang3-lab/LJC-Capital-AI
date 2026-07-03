# V8 FINAL Bug #002 - Data Refresh Guard

## 修复内容

- 检查 quotes.csv / capital.csv / portfolio.csv 是否存在
- 自动读取 CSV 日期字段
- 判断 quotes/capital 是否为今日数据
- War Room 顶部提示需要更新数据
- 数据导入页显示 CSV 文件状态
- 新增 `scripts/open_data_inbox.command`

## 发布冻结说明

此补丁属于 P0 验收修复：
防止历史 CSV 被误认为今日行情。
