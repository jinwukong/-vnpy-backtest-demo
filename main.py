import argparse
import logging
from modules.data_download import download_and_save_data
from modules.backtest_runner import run_backtest

# Configure logging (console level is INFO)
logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="VN Trader backtesting demo.")
    
    parser.add_argument("--symbol", type=str, default="MA2410", help="Futures symbol code, e.g. MA2410.")
    parser.add_argument("--exchange", type=str, default="CZCE", help="Exchange name, e.g. CZCE.")
    parser.add_argument("--start", type=str, default="2023-10-20", help="Start date (YYYY-MM-DD).")
    parser.add_argument("--end", type=str, default="2024-10-20", help="End date (YYYY-MM-DD).")
    parser.add_argument("--interval", type=str, default="1m", help="Data interval, e.g. 1m, 5m, 15m, 1d, etc.")
    parser.add_argument("--database", type=str, default="database.db", help="Path to the SQLite database file.")
    parser.add_argument("--capital", type=float, default=100000, help="Initial capital for backtesting.")
    
    args = parser.parse_args()

    # 1. Download and save data.
    logging.info("Start downloading data.")
    download_and_save_data(symbol=args.symbol,
                           exchange=args.exchange,
                           start=args.start,
                           end=args.end,
                           interval=args.interval,
                           db_path=args.database)

    # 2. Run backtest.
    logging.info("Start backtest.")
    run_backtest(symbol=args.symbol,
                 exchange=args.exchange,
                 start=args.start,
                 end=args.end,
                 interval=args.interval,
                 db_path=args.database,
                 capital=args.capital)

    logging.info("Backtest finished.")

if __name__ == "__main__":
    main()
