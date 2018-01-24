# coding:utf-8
from model.Object import Object


class Merge(Object):
    '''
    聚合行情 -24小时成交量数据
    '''

    def __init__(self, ts, tick, ch):
        '''
        :param ts:响应生成时间点，单位：毫秒
        :param tick:K线数据
        :param ch:数据所属的 channel，格式： market.$symbol.detail.merged
        '''
        self.ts = ts
        self.tick = tick
        self.ch = ch

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
