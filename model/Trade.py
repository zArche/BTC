# coding:utf-8
from model.Object import Object


class Trade(Object):
    '''
    交易记录
    '''

    class Tick(Object):
        class Data(Object):
            def __init__(self, id, price, amount, direction, ts):
                '''
                :param id:成交id
                :param price:成交价钱
                :param amount:成交量
                :param direction:主动成交方向
                :param ts:成交时间
                '''
                self.id = id
                self.price = price
                self.amount = amount
                self.direction = direction
                self.ts = ts

        def __init__(self, id, ts, data):
            self.id = id
            self.ts = ts
            self.data = data

    def __init__(self, ts, tick, ch):
        '''
        :param ts:响应生成时间点，单位：毫秒
        :param tick:Trade 数据
        :param ch:数据所属的 channel，格式： market.$symbol.trade.detail
        '''
        self.ts = ts
        self.tick = tick
        self.ch = ch
