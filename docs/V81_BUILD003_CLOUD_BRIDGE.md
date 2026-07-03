# V8.1 Build003 Cloud Bridge

## 目标

实现半云端实时架构：

Mac 本地采集数据 -> cloud/live_state.json -> Streamlit / 手机 / 云端读取

## 新增脚本

- `scripts/publish_cloud_bridge.command`
- `scripts/start_cloud_publisher.command`

## 桌面快捷方式

重新运行：

```bash
bash scripts/create_desktop_shortcuts.command
```

会新增：

- `LJC Publish Cloud.command`
- `LJC Cloud Publisher.command`

## 说明

当前版本先用 `cloud/live_state.json` 作为云桥文件。
后续可以替换为 Supabase / Firebase / S3 / GitHub Gist / 自有服务器。
