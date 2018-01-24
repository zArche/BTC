# coding:utf-8
from model.Object import Object


class Depth(Object):
    '''
    行情深度信息
    '''

    class Tick(Object):
        def __init__(self, bids, asks):
            '''
            :param bids: 买盘,[price(成交价), amount(成交量)], 按price降序
            :param asks:买盘,[price(成交价), amount(成交量)], 按price降序
            :return:
            '''
            self.bids = bids
            self.asks = asks

    def __init__(self, ts, tick, ch):
        '''
        :param ts:响应生成时间点，单位：毫秒
        :param tick:Depth 数据
        :param ch:数据所属的 channel，格式： market.$symbol.depth.$type
        '''
        self.ts = ts
        self.tick = tick
        self.ch = ch
