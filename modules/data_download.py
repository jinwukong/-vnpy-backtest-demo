import logging
import sys
from datetime import datetime

from vnpy_rqdata.rqdata_datafeed import RqdataDatafeed
from vnpy.trader.object import HistoryRequest
from vnpy.trader.constant import Exchange, Interval
from vnpy_sqlite.sqlite_database import SqliteDatabase

def download_and_save_data(symbol: str, 
                           exchange: str, 
                           start: str, 
                           end: str, 
                           interval: str, 
                           db_path: str):
    """
    Download historical data from RQData and save to SQLite database.
    """
    feed = RqdataDatafeed()
    
    if not feed.init():
        logging.error("Failed to initialize RQData feed.")
        sys.exit(1)
    
    # Determine the interval enum from a string like "1m", "5m", "1d"
    # This is a simple example, you can extend it to more intervals if needed.
    if interval.lower().endswith("m"):
        interval_enum = Interval.MINUTE
    else:
        interval_enum = Interval.DAILY
    
    # Convert exchange string (e.g. "CZCE") to vn.py Exchange enum if needed.
    try:
        exchange_enum = Exchange(exchange)
    except ValueError:
        logging.error(f"Unsupported Exchange: {exchange}")
        sys.exit(1)
    
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    
    req = HistoryRequest(
        symbol=symbol,
        exchange=exchange_enum,
        start=start_dt,
        end=end_dt,
        interval=interval_enum
    )
    
    bar_list = feed.query_bar_history(req)
    
    if not bar_list:
        logging.warning("No bar data found.")
        sys.exit(0)
    
    logging.info(f"Got {len(bar_list)} bar records from RQData.")
    
    db = SqliteDatabase(db_path=db_path)
    db.save_bar_data(bar_list)
    
    logging.info("Bar data saved to SQLite successfully.")
