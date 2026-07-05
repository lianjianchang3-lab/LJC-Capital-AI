# LJC V8.5 Build004 Fix DailyPlan

修复：
- Build002 页面卡在 Running load_all()
- 改为分段 safe_call 加载
- 关闭默认自动刷新
- 新增主入口 scripts/start_ljc_main.command

测试：
scripts/test_v8_5_build004.command

启动主系统：
scripts/start_ljc_main.command
