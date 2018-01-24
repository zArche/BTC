# coding:utf-8
from model.Object import Object


class Market(Object):
    """
    行情
    """

    class Tick(Object):
        '''
        行情数据
        '''

        def __init__(self, id, amount, count, open, close, low, high, vol):
            '''
            :param id:
            :param amount:成交量
            :param count:成交笔数
            :param open:开盘价
            :param close:收盘价-当前价
            :param low:最低价
            :param high:最高价
            :param vol:成交额(成交价 * 成交量)
            '''
            self.id = id
            self.amount = amount
            self.count = count
            self.open = open
            self.close = close
            self.low = low
            self.high = high
            self.vol = vol

    def __init__(self, ts, ticks, ch):
        '''
        :param ts:响应生成时间点，单位：毫秒
        :param ticks:KLine 数据
        :param ch:数据所属的 channel，格式： market.$symbol.kline.$period
        '''
        self.ts = ts
        self.ticks = ticks
        self.ch = ch
