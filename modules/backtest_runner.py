import logging
from datetime import datetime
import importlib

import pandas as pd
from vnpy_ctastrategy.backtesting import BacktestingEngine
from vnpy.trader.constant import Interval, Exchange
from vnpy_sqlite.sqlite_database import SqliteDatabase

def run_backtest(symbol: str,
                 exchange: str,
                 start: str,
                 end: str,
                 interval: str,
                 db_path: str,
                 capital: float):
    """
    Load historical data from SQLite and run backtesting with a specified strategy.
    """
    # 1. Dynamically import strategy. (You can configure the strategy name in code or in config files.)
    name = "strategies.double_ma_demo2"
    modules = importlib.import_module(name)
    strategy_class = getattr(modules, "avg2")  # e.g. 'avg2' is the class name in double_ma_demo2.py

    # 2. Create backtesting engine
    bkt = BacktestingEngine()
    
    # 3. Determine interval
    if interval.lower().endswith("m"):
        interval_enum = Interval.MINUTE
    else:
        interval_enum = Interval.DAILY
    
    # 4. Convert exchange to enum
    try:
        exchange_enum = Exchange(exchange)
    except ValueError:
        logging.error(f"Unsupported Exchange: {exchange}")
        return
    
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    
    # 5. Set parameters
    bkt.set_parameters(
        vt_symbol=f"{symbol}.{exchange}",
        interval=interval_enum,
        start=start_dt,
        end=end_dt,
        rate=0,
        slippage=0,
        size=10,
        pricetick=1,
        capital=capital,
        database_url=f"sqlite:///{db_path}"
    )
    
    # 6. Add strategy
    bkt.add_strategy(strategy_class=strategy_class, setting={})
    
    # 7. Load data
    bkt.load_data()
    logging.info(f"Data loaded: {len(bkt.history_data)} bars.")
    
    # 8. Run backtesting
    bkt.run_backtesting()
    
    # 9. Calculate results
    df: pd.DataFrame = bkt.calculate_result()
    df.to_csv("test.csv", index=False)
    logging.info("Backtest results saved to test.csv.")
    
    # 10. Calculate statistics
    stats = bkt.calculate_statistics(df)
    logging.info("Backtest statistics:")
    logging.info(stats)
    
    # 11. Visualization
    fig = bkt.show_chart(df)
    fig.show()
