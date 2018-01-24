# coding:utf-8

from ApiClient import ApiClient
from model.Symbol import Symbol
from policy.KDJ import KDJ
import xlwt
import time


def test_market(client, symbol, period, size):
    '''
    行情API测试
    '''
    market = client.get_kline(symbol, period, size)
    return market


def test_merge(client, symbol):
    '''
    聚合行情测试
    '''
    merge = client.get_merged_tickers(symbol)
    return merge


def test_depth(client, symbol, type):
    '''
    深度图信息
    '''
    depth = client.get_depth(symbol, type)
    return depth


def test_trade(client, symbol):
    '''
    交易详情
    '''
    trade = client.get_trade_detail(symbol)

    return trade


def test_account(client):
    '''
    账户
    '''
    accounts = client.get_all_accounts()
    return accounts


def test_balance(client, account_id):
    '''
    余额
    '''
    balances = client.get_balance(account_id)
    return balances


def test_send_order(client, amount, symbol, type, price=0):
    '''
    下单
    '''
    order = client.send_order(amount, symbol, type, price)
    return order


def test_cancle_order(client, order_id):
    '''
    撤单
    '''
    client.cancel_order(order_id)


def test_order_detail(client, order_id):
    '''
    订单详情
    '''
    order = client.get_order_detail(order_id)
    return order


def test_order_list(client, symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None,
                    size=None):
    '''
    历史订单条件查询
    '''
    orders = client.get_all_orders(symbol, states, types, start_date, end_date, _from, direct, size)
    return orders


def test_transfer_balance_from_spot_to_loan(client, symbol, currency, amount):
    '''
    从交易账户转移到借贷账户
    '''
    client.transfer_balance_from_spot_to_loan(symbol, currency, amount)


def test_tratransfer_balance_from_loan_to_spot(client, symbol, currency, amount):
    '''
    从借贷账户转移到交易账户
    '''
    client.tratransfer_balance_from_loan_to_spot(symbol, currency, amount)


def test_apply_for_loan(client, symbol, currency, amount):
    '''
    借贷
    '''
    order = client.apply_for_loan(symbol, currency, amount)
    return order


def test_repay_loan(client, order_id, amount):
    '''
    偿还借贷
    '''
    client.repay_loan(order_id, amount)


def test_get_loan_orders(client, symbol, currency, start_date=None, end_date=None,
                         states=None, _from=None, direct=None, size=None):
    '''
    查询所有借贷订单
    '''
    orders = client.get_loan_orders(symbol, currency, start_date, end_date,
                                    states, _from, direct, size)
    return orders


def test_kdj(ticks):
    '''
    KDJ策略测试
    '''
    kdj = KDJ(ticks)
    return kdj


from matplotlib import pyplot as plt

if __name__ == "__main__":

    client = ApiClient()

    symbol = Symbol(Symbol.BTC, Symbol.USDT).get_symbol()

    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet("sheet1", True)
    sheet.write(0, 0, "时间")
    sheet.write(0, 1, "开盘价")
    sheet.write(0, 2, "收盘价")
    sheet.write(0, 3, "最低价")
    sheet.write(0, 4, "最高价")
    sheet.write(0, 5, "成交量")
    sheet.write(0, 6, "成交笔数")
    sheet.write(0, 7, "成交总额")
    sheet.write(0, 8, "KDJ")

    indexs = []
    ks = []
    ds = []
    js = []

    i = 0
    while i < 30:
        i = i + 1  # 从第一列开始
        market = test_market(client, symbol, "1min", "9")

        ticks = market.ticks[::-1]  # 倒序翻转

        print "=" * 40 + "近期行情" + "=" * 40

        for tick in ticks:
            print tick

        print "=" * 88

        print "\n\n"

        kdj = test_kdj(ticks)

        tick = ticks[-1]
        print "-" * 40 + "KDJ信息" + "-" * 40
        print "当前点行情:" + str(tick)
        print "[k,d,j] -> [%s,%s,%s]" % (kdj.k, kdj.d, kdj.j)
        print "-" * 87

        sheet.write(i, 0,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        sheet.write(i, 1, tick.open)
        sheet.write(i, 2, tick.close)
        sheet.write(i, 3, tick.low)
        sheet.write(i, 4, tick.high)
        sheet.write(i, 5, tick.amount)
        sheet.write(i, 6, tick.count)
        sheet.write(i, 7, tick.vol)
        sheet.write(i, 8, "[%s,%s,%s]" % (kdj.k, kdj.d, kdj.j))

        workbook.save("/Users/arche/Desktop/a.xls")

        indexs.append(i)
        ks.append(kdj.k)
        ds.append(kdj.d)
        js.append(kdj.j)
        time.sleep(1)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.suptitle("KDJ", fontsize=14, fontweight='bold')

    ax.plot(indexs, ks)
    ax.plot(indexs, ds)
    ax.plot(indexs, js)

    plt.legend(('K', 'D', 'J'))
    plt.grid(True)
    plt.show()

