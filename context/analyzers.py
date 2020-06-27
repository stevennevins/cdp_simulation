from backtrader import Analyzer
from backtrader.utils import AutoOrderedDict

import pandas as pd

class coll_ratio(Analyzer):
    alias = ('collatarization_ratio',)

    def create_analysis(self):
        '''Replace default implementation to instantiate an AutoOrdereDict
        rather than an OrderedDict'''
        self.rets = AutoOrderedDict()

    def start(self):
        super(coll_ratio,self).start()
        self.coll_ratio_list = dict()

    def next(self):
        self.coll_ratio_list[self.data.datetime.datetime()]=self.strategy.coll_ratio

    def stop(self):
        self.rets.coll_ratios = pd.DataFrame(self.coll_ratio_list.items())


class amt_eth(Analyzer):
    alias = ('amount_eth',)

    def create_analysis(self):
        '''Replace default implementation to instantiate an AutoOrdereDict
        rather than an OrderedDict'''
        self.rets = AutoOrderedDict()

    def start(self):
        super(amt_eth,self).start()
        self.amt_eth = dict()

    def next(self):
        self.amt_eth[self.data.datetime.datetime()]=self.strategy.broker.getposition(self.data).size

    def stop(self):
        self.rets.amt_eth = pd.DataFrame(self.amt_eth.items())