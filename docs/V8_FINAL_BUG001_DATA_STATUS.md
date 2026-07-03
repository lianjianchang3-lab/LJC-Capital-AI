# V8 FINAL Bug #001 - Data Status Center

## 修复内容

- 顶部增加 Data Status Center
- 明确显示当前模式：CSV TEST MODE / LIVE MODE
- 显示数据来源、Provider、数据日期、文件更新时间
- 如果数据不是今日或不是实时，红色警告
- Health 页面显示 Realtime / Provider / Freshness

## 目的

避免用户误把本地 CSV / 示例数据当作实时行情用于实盘决策。

## V8.0 Release Freeze 说明

此补丁属于 P0 可用性与安全性修复，不属于新增功能。
