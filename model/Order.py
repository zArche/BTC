# coding:utf-8
from model.Object import Object


class Order(Object):
    def __init__(self, id = None, symbol=None, account_id=None, amount=None, price=None, created_at=None, type=None,
                 field_amount=None,
                 field_cash_amount=None, field_fees=None, finished_at=None, source=None, state=None,
                 canceled_at=None):
        '''
        :param id:订单ID
        :param symbol:交易对
        :param account_id:账户 ID
        :param amount:订单数量
        :param price:订单价格
        :param created_at:订单创建时间
        :param type:订单类型 buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖
        :param field_amount:已成交数量
        :param field_cash_amount:已成交总金额
        :param field_fees:已成交手续费（买入为币，卖出为钱）
        :param finished_at:最后成交时间
        :param source:订单来源
        :param state:订单状态 pre-submitted 准备提交, submitting , submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销
        :param canceled_at:订单撤销时间
        '''
        self.id = id
        self.symbol = symbol
        self.account_id = account_id
        self.amount = amount
        self.price = price
        self.created_at = created_at
        self.type = type
        self.field_amount = field_amount
        self.field_cash_amount = field_cash_amount
        self.field_fees = field_fees
        self.finished_at = finished_at
        self.source = source
        self.state = state
        self.canceled_at = canceled_at
