# V8.1 Build031-070 UI Integration Fix

## 修复内容

- 将 Build031-070 Strategy Workbench 明确挂载到 `app.py`
- 新增 7 个页面：
  - Master V3
  - Entry / Exit
  - Score V3
  - Selection
  - Portfolio V3
  - Daily Workbench
  - Report Export

此前 Build031-070 后端模块已经安装成功，但主界面没有显示入口。
本补丁只做 UI 挂载，不修改底层决策逻辑。
