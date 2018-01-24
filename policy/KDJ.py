# coding:utf-8
from model.Object import Object


class KDJ(Object):
    '''
    KDJ策略
    '''

    def __init__(self, ticks):
        '''
        :param ticks: 当前点前N个点的数据 @Market.ticks
        '''

        highs = []
        lows = []

        for tick in ticks:
            highs.append(tick.high)
            lows.append(tick.low)

        self.high = max(highs)  # 周期内最高价
        self.low = min(lows)  # 周期内最低价

        period = len(ticks)  # 周期长度

        pk = 50  # 当前离散点的前一个点K值  默认为50
        pd = 50  # 当前离散点的前一个点D值  默认为50

        k = 0
        d = 0
        j = 0

        for i in range(0, period):
            tick = ticks[i]  # 第i个离散点的具体数据内容
            rsv = 1.0 * (tick.close - self.low) / (self.high - self.low) * 100  # 第i个离散点的随机指标
            k = 2.0 / 3 * pk + 1.0 / 3 * rsv
            d = 2.0 / 3 * pd + 1.0 / 3 * k
            j = 3.0 * k - 2.0 * d

            pk = k
            pd = d

        self.k = k
        self.d = d
        self.j = j
