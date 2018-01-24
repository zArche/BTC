# coding:utf-8
from model.Object import Object


class Balance(Object):
    def __init__(self, balance, currency, type):
        '''
        :param balance:余额
        :param currency:币种
        :param type:类型 trade: 交易余额，frozen: 冻结余额
        '''
        self.balance = balance
        self.currency = currency
        self.type = type
