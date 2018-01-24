# coding:utf-8

from model.Account import Account
from model.Balance import Balance
from model.Depth import Depth
from model.LoanOrder import LoanOrder
from model.Market import Market
from model.Merge import Merge
from model.Order import Order
from model.Trade import Trade
from service.HuobiService import *


class ApiClient:
    def get_kline(self, symbol, period, size):
        '''
        获取行情k线
        :param symbol:交易对 btcusdt, bccbtc, rcneth ...
        :param period: K线类型 1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
        :param size: 获取数量 默认值150,[1,2000]
        :return:
        '''
        json = get_kline(symbol, period, size)

        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        data = json["data"]

        ticks = []
        for d in data:
            id = d["id"]
            amount = d["amount"]
            count = d["count"]
            open = d["open"]
            close = d["close"]
            low = d["low"]
            high = d["high"]
            vol = d["vol"]

            tick = Market.Tick(id, amount, count, open, close, low, high, vol)

            ticks.append(tick)

        ts = json["ts"]
        ch = json["ch"]
        market = Market(ts, ticks, ch)
        return market

    def get_merged_tickers(self, symbol):
        '''
        获取24小时聚合行情
        :param symbol:
        :return:
        '''
        json = get_detail(symbol)

        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        ts = json["ts"]
        ch = json["ch"]
        d = json["tick"]

        id = d["id"]
        amount = d["amount"]
        count = d["count"]
        open = d["open"]
        close = d["close"]
        low = d["low"]
        high = d["high"]
        vol = d["vol"]

        tick = Merge.Tick(id, amount, count, open, close, low, high, vol)
        merge = Merge(ts, tick, ch)
        return merge

    def get_depth(self, symbol, type):
        '''
        获取深度图信息
        :param symbol:交易对
        :param type:Depth 类型 step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
        :return:
        '''

        json = get_depth(symbol, type)

        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        ts = json["ts"]
        ch = json["ch"]
        data = json["tick"]

        bids = data["bids"]
        asks = data["asks"]

        tick = Depth.Tick(bids, asks)

        depth = Depth(ts, tick, ch)
        return depth

    def get_trade_detail(self, symbol):
        json = get_trade(symbol)

        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None
        ts = json["ts"]
        ch = json["ch"]

        t = json["tick"]

        id = t["id"]
        ts1 = t["ts"]

        dd = t["data"]
        datas = []
        for d in dd:
            id1 = d["id"]
            price = d["price"]
            amount = d["amount"]
            direction = d["direction"]
            ts2 = d["ts"]
            data = Trade.Tick.Data(id1, price, amount, direction, ts2)

            datas.append(data)
        tick = Trade.Tick(id, ts1, datas)

        trade = Trade(ts, tick, ch)
        return trade

    def get_all_accounts(self):
        '''
        获取所有账户信息
        :return:
        '''
        accounts = []
        json = get_accounts()

        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        data = json["data"]
        for d in data:
            id = d["id"]
            state = d["state"]
            type = d["type"]
            subtype = d["subtype"]

            account = Account(id, state, type, subtype)
            accounts.append(account)

        return accounts

    def get_balance(self, id):
        json = get_balance(id)
        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        data = json["data"]
        list = data["list"]

        balances = []

        for d in list:
            currency = d["currency"]
            type = d["type"]
            balance = d["balance"]

            balance = Balance(balance, currency, type)

            balances.append(balance)

        return balances

    def send_order(self, amount, symbol, type, price=0):
        """
        :param amount:
        :param symbol:
        :param type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price:
        :return:
        """
        json = send_order(amount, "api", symbol, type, price)
        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        id = json["data"]
        order = Order(id)
        return order

    def cancel_order(self, order_id):
        cancel_order(order_id)

    def get_order_detail(self, order_id):
        json = order_info(order_id)
        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        order = Order()

        data = json["data"]
        order.id = data["id"]
        order.symbol = data["symbol"]
        order.account_id = data["account-id"]
        order.amount = data["amount"]
        order.price = data["price"]
        order.created_at = data["created-at"]
        order.type = data["type"]
        order.field_amount = data["field-amount"]
        order.field_cash_amount = data["field-cash-amount"]
        order.field_fees = data["field-fees"]
        order.finished_at = data["finished-at"]
        order.source = data["source"]
        order.state = data["state"]
        order.canceled_at = data["canceled-at"]

        return order

    def get_all_orders(self, symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None,
                       size=None):
        '''
        :param symbol:交易对
        :param types:查询的订单类型组合，使用','分割 [buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖]
        :param states:查询的订单状态组合，使用','分割 [pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销]
        :param start_date:查询开始日期, 日期格式yyyy-mm-dd
        :param end_date:查询结束日期, 日期格式yyyy-mm-dd
        :param _from:查询起始 ID
        :param direct:查询方向 [prev 向前，next 向后]
        :param size:查询记录大小
        :return:
        '''

        json = orders_list(symbol, states, types, start_date, end_date, _from, direct, size)
        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        orders = []
        data = json["data"]
        for d in data:
            order = Order()
            order.id = d["id"]
            order.symbol = d["symbol"]
            order.account_id = d["account-id"]
            order.amount = d["amount"]
            order.price = d["price"]
            order.created_at = d["created-at"]
            order.type = d["type"]
            order.field_amount = d["field-amount"]
            order.field_cash_amount = d["field-cash-amount"]
            order.field_fees = d["field-fees"]
            order.finished_at = d["finished-at"]
            order.source = d["source"]
            order.state = d["state"]
            order.created_at = d["canceled-at"]

            orders.append(order)

        return orders

    def transfer_balance_from_spot_to_loan(self, symbol, currency, amount):
        '''
        从交易账户转移资产到借贷账户
        :param symbol:交易对
        :param currency:币种
        :param amount:金额
        :return:
        '''
        json = exchange_to_margin(symbol, currency, amount)
        if json["status"] != "ok":
            print "Error:", json["err-msg"]

    def tratransfer_balance_from_loan_to_spot(self, symbol, currency, amount):
        '''
        从借贷账户转移资产到交易账户
        :param symbol:交易对
        :param currency:币种
        :param amount:金额
        :return:
        '''
        json = margin_to_exchange(symbol, currency, amount)
        if json["status"] != "ok":
            print "Error:", json["err-msg"]

    def apply_for_loan(self, symbol, currency, amount):
        '''
        申请借贷
        :param symbol:交易对
        :param currency:币种
        :param amount:金额
        :return:
        '''
        json = get_margin(symbol, currency, amount)
        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        id = json["data"]
        order = Order(id)
        return order

    def repay_loan(self, order_id, amount):
        '''
        :param order_id:
        :param amount:金额
        :return:
        '''
        json = repay_margin(order_id, amount)
        if json["status"] != "ok":
            print "Error:", json["err-msg"]

    def get_loan_orders(self, symbol, currency, start_date=None, end_date=None,
                        states=None, _from=None, direct=None, size=None):
        json = loan_orders(symbol, currency, start_date, end_date, _from, direct, size)
        if json["status"] != "ok":
            print "Error:", json["err-msg"]
            return None

        orders = []
        data = json["data"]
        for d in data:
            loan_order = LoanOrder()
            loan_order.currency = d["currency"]
            loan_order.symbol = d["symbol"]
            loan_order.accrued_at = d["accrued-at"]
            loan_order.loan_amount = d["loan-amount"]
            loan_order.loan_balance = d["loan-balance"]
            loan_order.interest_balance = d["interest-balance"]
            loan_order.created_at = d["created-at"]
            loan_order.interest_amount = d["interest-amount"]
            loan_order.interest_rate = d["interest-rate"]
            loan_order.account_id = d["account-id"]
            loan_order.user_id = d["user-id"]
            loan_order.id = d["id"]
            loan_order.state = d["state"]

            orders.append(loan_order)
        return orders

