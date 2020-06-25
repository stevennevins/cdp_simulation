import backtrader as bt
import backtrader.indicators as btind

from ccxt_datahandler import ccxt_datahandler

class cdp_sim(bt.Strategy):

    params = dict(
        verbose=True,
        a_upper = 2.2,
        a_lower = 1.8,
        a_target = 2,
        na_upper = 3.5,
        na_lower = 2.5,
        na_target = 3,
        period=14,
    )
    def __init__(self):
        ##set up indicators add stop trailer and cross condition for stochasticsubmit(False)
        self.RSI = btind.RSI(period=self.p.period)

    def start(self):
        self.debt = 0
        self.target = self.p.a_target
        self.lower = self.p.a_lower
        self.upper = self.p.a_upper
    @property
    def price(self):
        return self.data
    @property
    def usd_pos(self):
        return self.broker.getposition(self.data).size*self.price
    @property
    def coll_ratio(self):
        return self.usd_pos/self.debt if self.debt else 0
    def boost(self):
        coll_before = self.usd_pos
        x = (coll_before - self.target * self.debt)/(self.target-1)
        self.debt += x
        self.buy(size=x/self.price)
    def repay(self):
        coll_before = self.usd_pos
        x = (coll_before - self.target * self.debt)/(self.target+1)*-1
        self.debt -= x
        self.sell(size=x/self.price)
    def set_ratios(self):
        if self.RSI > 60:
            self.target = self.p.a_target
            self.lower = self.p.a_lower
            self.upper = self.p.a_upper
        else:
            self.target = self.p.na_target
            self.lower = self.p.na_lower
            self.upper = self.p.na_upper
    def stop(self):
        self.stop_val = self.usd_pos
        self.pnl_val = self.usd_pos - self.start_val
        self.log('Start Value: {:.2f}', self.start_val)
        self.log('Final Value: {:.2f}', self.stop_val)
        self.log('PNL   Value: {:.2f}', self.pnl_val)
    
    def next(self):
        self.logdata()
        self.set_ratios()
        if not self.coll_ratio:
            ##initializing position
            self.buy(size=10)
            self.debt = self.data * 10 / self.target
            self.start_val = self.data*10
        elif self.coll_ratio > self.upper:
            self.boost()
        elif self.coll_ratio < self.lower:
            self.repay()


    def logdata(self):
        if self.p.verbose:  # logging
            txt = []
            txt += ['{:.2f}'.format(self.position.size)]
            txt += ['{:.2f}'.format(self.data.open[0])]
            txt += ['{:.2f}'.format(self.data.high[0])]
            txt += ['{:.2f}'.format(self.data.low[0])]
            txt += ['{:.2f}'.format(self.data.close[0])]
            self.log(','.join(txt))
            txt = []
            txt += ['Coll_Ratio {:.2f}'.format(self.coll_ratio)]
            txt += ['Lower {:.2f}'.format(self.lower)]
            txt += ['Target {:.2f}'.format(self.target)]
            txt += ['Upper {:.2f}'.format(self.upper)]
            self.log(','.join(txt))


    def log(self, txt, *args):
        if self.p.verbose:
            out = [self.datetime.date().isoformat(), txt.format(*args)]
            print(','.join(out))


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(cdp_sim)
    cerebro.broker.setcash(1000000000000000000000000000000)
    cerebro.adddata(bt.feeds.PandasData(dataname=ccxt_datahandler('ETH/USDT', 'poloniex', '1d')))
    strat = cerebro.run()[0]
    cerebro.plot()