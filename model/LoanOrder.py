# coding:utf-8

from model.Object import Object


class LoanOrder(Object):

    def __init__(self, id=None, user_id=None, account_id=None, symbol=None,
                 currency=None, loan_amount=None, loan_balance=None,
                 interest_rate=None, interest_amount=None, interest_balance=None,
                 created_at=None, accrued_at=None, state=None):
        '''
        :param id:订单号
        :param user_id:用户ID
        :param account_id:账户ID
        :param symbol:交易对
        :param currency:币种
        :param loan_amount:借贷本金总额
        :param loan_balance:未还本金
        :param interest_rate:利率
        :param interest_amount:利息总额
        :param interest_balance:未还利息
        :param created_at:借贷发起时间
        :param accrued_at:最近一次计息时间
        :param state:订单状态 [created 未放款，accrual 已放款，cleared 已还清，invalid 异常]
        '''
        self.id = id
        self.user_id = user_id
        self.account_id = account_id
        self.symbol = symbol
        self.currency = currency
        self.loan_amount = loan_amount
        self.loan_balance = loan_balance
        self.interest_rate = interest_rate
        self.interest_amount = interest_amount
        self.interest_balance = interest_balance
        self.created_at = created_at
        self.accrued_at = accrued_at
        self.state = state


