# LJC Capital AI Pro V8.5 Final

统一交易驾驶舱，包含市场状态、执行建议、自选股、持仓、风险和手机端。

## 桌面端启动

```bash
scripts/start_desktop.command
```

## 手机端启动

```bash
scripts/start_mobile.command
```

手机和电脑需要连接同一个 Wi-Fi。手机访问终端显示的 Network URL，例如：

```text
http://192.168.0.27:8501
```

## 检查

```bash
scripts/check_environment.command
scripts/check_release.command
```

## 自选股

```text
data/watchlist/watchlist.csv
```

列：

```text
code,name,note
```

## 持仓

```text
data/portfolio/holdings.csv
```

列：

```text
code,name,shares,cost
```
