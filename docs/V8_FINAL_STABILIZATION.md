# V8.0 Final Stabilization

本补丁完成：

- 统一 Data Gateway
- 统一 Quote / Capital / Signal 模型
- 修复 app.py 中 tab8/tab9 未定义导致的启动风险
- Dashboard 改为只读取 Gateway 与 AI 输出
- 保留 CSV 导入，但不让 AI 直接读取散乱数据
- 为后续商业实时 Provider 预留入口

V8.0 进入 Release Stabilization，只修：
- 实时数据
- Gateway
- AI计算
- 稳定性
