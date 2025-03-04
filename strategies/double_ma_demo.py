from vnpy_ctastrategy import CtaTemplate, BarData
from vnpy.trader.object import TickData

class avg(CtaTemplate):
    """
    A demo strategy for double MA cross.
    """
    author = "Your Name"
    
    fast_window = 10
    slow_window = 20
    
    fast_ma = 0
    slow_ma = 0
    
    fast_buffer = []
    slow_buffer = []
    
    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma", "slow_ma"]
    
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
    
    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("Strategy initialized.")
        self.load_bar(10)  # Load some bars to calculate MAs if needed.
    
    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("Strategy started.")
    
    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("Strategy stopped.")
    
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        pass
    
    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.fast_buffer.append(bar.close_price)
        self.slow_buffer.append(bar.close_price)
        
        if len(self.fast_buffer) > self.fast_window:
            self.fast_buffer.pop(0)
        if len(self.slow_buffer) > self.slow_window:
            self.slow_buffer.pop(0)
        
        # Calculate fast & slow MAs
        if len(self.fast_buffer) == self.fast_window:
            self.fast_ma = sum(self.fast_buffer) / self.fast_window
        if len(self.slow_buffer) == self.slow_window:
            self.slow_ma = sum(self.slow_buffer) / self.slow_window
        
        # Generate signals
        if self.fast_ma and self.slow_ma:
            if self.fast_ma > self.slow_ma and not self.pos:
                self.buy(bar.close_price, 1)
            elif self.fast_ma < self.slow_ma and self.pos > 0:
                self.sell(bar.close_price, 1)
        
        self.put_event()
