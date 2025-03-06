# vnpy-backtest-demo

一个基于 [vnpy](https://github.com/vnpy/vnpy) 框架的无界面回测项目，用于演示如何通过 RQData 下载期货历史数据并保存到本地 SQLite 数据库，再使用自定义策略进行回测,可提升运行速度。
为本人2024.12在某基金量化部门实习时的所完成,和公司达成一致后开源.

## 功能

- 通过 RQData 获取分钟或日级别历史数据。
- 将数据存储到本地 SQLite 数据库。
- 使用 `vnpy_ctastrategy.backtesting.BacktestingEngine` 进行回测。
- 动态导入自定义策略（存放在 `strategies` 目录下）。
- 生成 CSV 回测结果，并通过图表展示交易信号和资金曲线。
