# coding:utf-8
import Config
from ApiClient import ApiClient
from dao.TickDao import TickDao
from model.Symbol import Symbol
from policy.KDJ import KDJ
import xlwt
import time
from matplotlib import pyplot as plt, animation

from util import KDJUtil


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


def get_1min_data(client, symbol, size):
    market = test_market(client, symbol, "1min", size)
    return market


def get_15min_data(client, symbol, size):
    market = test_market(client, symbol, "15min", size)
    return market


def get_60min_data(client, symbol, size):
    market = test_market(client, symbol, "60min", size)
    return market


def save_excel(ticks, kdjs, path):
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

    for i in range(0, len(ticks)):
        tick = ticks[i]
        kdj = kdjs[i]

        sheet.write(i, 0, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        sheet.write(i, 1, tick.open)
        sheet.write(i, 2, tick.close)
        sheet.write(i, 3, tick.low)
        sheet.write(i, 4, tick.high)
        sheet.write(i, 5, tick.amount)
        sheet.write(i, 6, tick.count)
        sheet.write(i, 7, tick.vol)
        sheet.write(i, 8, "[%s,%s,%s]" % (kdj.k, kdj.d, kdj.j))

    workbook.save(path)


def init():
    global xs_of_1min
    global ks_of_1min
    global ds_of_1min
    global js_of_1min

    global xs_of_15min
    global ks_of_15min
    global ds_of_15min
    global js_of_15min

    global xs_of_60min
    global ks_of_60min
    global ds_of_60min
    global js_of_60min

    num = 60  # 绘制最近60个点
    period = 9  # JDK随机指标计算周期

    markets_of_1min = get_1min_data(client, symbol, num + period)
    markets_of_15min = get_15min_data(client, symbol, num + period)
    markets_of_60min = get_60min_data(client, symbol, num + period)

    ticks_of_1min = markets_of_1min.ticks[::-1]  # 倒序翻转
    ticks_of_15min = markets_of_15min.ticks[::-1]  # 倒序翻转
    ticks_of_60min = markets_of_60min.ticks[::-1]  # 倒序翻转

    ticks_of_1min, kdjs_of_1min = KDJUtil.kdj(ticks_of_1min, period)
    ticks_of_15min, kdjs_of_15min = KDJUtil.kdj(ticks_of_15min, period)
    ticks_of_60min, kdjs_of_60min = KDJUtil.kdj(ticks_of_60min, period)

    dao.insert(TABLE_NAME, ticks_of_1min, kdjs_of_1min, "1min")
    dao.insert(TABLE_NAME, ticks_of_15min, kdjs_of_15min, "15min")
    dao.insert(TABLE_NAME, ticks_of_60min, kdjs_of_60min, "60min")

    for i in range(0, len(ticks_of_1min)):
        xs_of_1min.append(i)
        ks_of_1min.append(kdjs_of_1min[i].k)
        ds_of_1min.append(kdjs_of_1min[i].d)
        js_of_1min.append(kdjs_of_1min[i].j)

    for i in range(0, len(ticks_of_15min)):
        xs_of_15min.append(i)
        ks_of_15min.append(kdjs_of_15min[i].k)
        ds_of_15min.append(kdjs_of_15min[i].d)
        js_of_15min.append(kdjs_of_15min[i].j)

    for i in range(0, len(ticks_of_60min)):
        xs_of_60min.append(i)
        ks_of_60min.append(kdjs_of_60min[i].k)
        ds_of_60min.append(kdjs_of_60min[i].d)
        js_of_60min.append(kdjs_of_60min[i].j)

    line_k_of_1min.set_data(xs_of_1min, ks_of_1min)
    line_d_of_1min.set_data(xs_of_1min, ds_of_1min)
    line_j_of_1min.set_data(xs_of_1min, js_of_1min)

    line_k_of_15min.set_data(xs_of_15min, ks_of_15min)
    line_d_of_15min.set_data(xs_of_15min, ds_of_15min)
    line_j_of_15min.set_data(xs_of_15min, js_of_15min)

    line_k_of_60min.set_data(xs_of_60min, ks_of_60min)
    line_d_of_60min.set_data(xs_of_60min, ds_of_60min)
    line_j_of_60min.set_data(xs_of_60min, js_of_60min)

    return line_k_of_1min, line_d_of_1min, line_j_of_1min, \
           line_k_of_15min, line_d_of_15min, line_j_of_15min, \
           line_k_of_60min, line_d_of_60min, line_j_of_60min


def animate(i):
    global xs_of_1min
    global ks_of_1min
    global ds_of_1min
    global js_of_1min

    global xs_of_15min
    global ks_of_15min
    global ds_of_15min
    global js_of_15min

    global xs_of_60min
    global ks_of_60min
    global ds_of_60min
    global js_of_60min

    period = 9  # JDK随机指标计算周期

    markets_of_1min = get_1min_data(client, symbol, period)
    markets_of_15min = get_15min_data(client, symbol, period)
    markets_of_60min = get_60min_data(client, symbol, period)

    ticks_of_1min = markets_of_1min.ticks[::-1]  # 倒序翻转
    ticks_of_15min = markets_of_15min.ticks[::-1]  # 倒序翻转
    ticks_of_60min = markets_of_60min.ticks[::-1]  # 倒序翻转

    ticks_of_1min, kdjs_of_1min = KDJUtil.kdj(ticks_of_1min, period)
    ticks_of_15min, kdjs_of_15min = KDJUtil.kdj(ticks_of_15min, period)
    ticks_of_60min, kdjs_of_60min = KDJUtil.kdj(ticks_of_60min, period)

    dao.insert(TABLE_NAME, ticks_of_1min, kdjs_of_1min, "1min")
    dao.insert(TABLE_NAME, ticks_of_15min, kdjs_of_15min, "15min")
    dao.insert(TABLE_NAME, ticks_of_60min, kdjs_of_60min, "60min")

    if i % 60 != 0:  # 1min内只更新
        xs_of_1min = xs_of_1min[0:-1]
        ks_of_1min = ks_of_1min[0:-1]
        ds_of_1min = ds_of_1min[0:-1]
        js_of_1min = js_of_1min[0:-1]

    xs_of_1min.append(1 + len(xs_of_1min))
    ks_of_1min.append(kdjs_of_1min[0].k)
    ds_of_1min.append(kdjs_of_1min[0].d)
    js_of_1min.append(kdjs_of_1min[0].j)
    ax_1min_kdj.set_xlim(len(xs_of_1min) - 60, len(xs_of_1min))

    if i % (60 * 15) != 0:  # 15min内只更新
        xs_of_15min = xs_of_15min[0:-1]
        ks_of_15min = ks_of_15min[0:-1]
        ds_of_15min = ds_of_15min[0:-1]
        js_of_15min = js_of_15min[0:-1]

    xs_of_15min.append(1 + len(xs_of_15min))
    ks_of_15min.append(kdjs_of_15min[0].k)
    ds_of_15min.append(kdjs_of_15min[0].d)
    js_of_15min.append(kdjs_of_15min[0].j)
    ax_15min_kdj.set_xlim(len(xs_of_15min) - 60, len(xs_of_15min))

    if i % (60 * 60) != 0:  # 60min内只更新
        xs_of_60min = xs_of_60min[0:-1]
        ks_of_60min = ks_of_60min[0:-1]
        ds_of_60min = ds_of_60min[0:-1]
        js_of_60min = js_of_60min[0:-1]

    xs_of_60min.append(1 + len(xs_of_60min))
    ks_of_60min.append(kdjs_of_60min[0].k)
    ds_of_60min.append(kdjs_of_60min[0].d)
    js_of_60min.append(kdjs_of_60min[0].j)
    ax_60min_kdj.set_xlim(len(xs_of_60min) - 60, len(xs_of_60min))

    line_k_of_1min.set_data(xs_of_1min, ks_of_1min)
    line_d_of_1min.set_data(xs_of_1min, ds_of_1min)
    line_j_of_1min.set_data(xs_of_1min, js_of_1min)

    line_k_of_15min.set_data(xs_of_15min, ks_of_15min)
    line_d_of_15min.set_data(xs_of_15min, ds_of_15min)
    line_j_of_15min.set_data(xs_of_15min, js_of_15min)

    line_k_of_60min.set_data(xs_of_60min, ks_of_60min)
    line_d_of_60min.set_data(xs_of_60min, ds_of_60min)
    line_j_of_60min.set_data(xs_of_60min, js_of_60min)

    return line_k_of_1min, line_d_of_1min, line_j_of_1min, \
           line_k_of_15min, line_d_of_15min, line_j_of_15min, \
           line_k_of_60min, line_d_of_60min, line_j_of_60min


if __name__ == "__main__":
    dao = TickDao(Config.HOST_NAME, Config.USER_NAME, Config.PASSWORD, Config.DATA_BASE_NAME)

    TABLE_NAME = "ticks"

    fig = plt.figure(figsize=(12, 9), dpi=72, facecolor="white")

    ax_1min_kdj = fig.add_subplot(3, 1, 1, xlim=(0, 60), ylim=(-10, 120))  # 1min KDJ 线
    ax_1min_kdj.set_title("1Min KDJ")

    ax_15min_kdj = fig.add_subplot(3, 1, 2, xlim=(0, 60), ylim=(-10, 120))  # 15min KDJ线
    ax_15min_kdj.set_title("15Min KDJ")

    ax_60min_kdj = fig.add_subplot(3, 1, 3, xlim=(0, 60), ylim=(-10, 120))  # 60min KDJ线
    ax_60min_kdj.set_title("60Min KDJ")

    line_k_of_1min, = ax_1min_kdj.plot([], [], lw=2)  # 1min KDJ K线
    line_d_of_1min, = ax_1min_kdj.plot([], [], lw=2)  # 1min KDJ D线
    line_j_of_1min, = ax_1min_kdj.plot([], [], lw=2)  # 1min KDJ J线

    line_k_of_15min, = ax_15min_kdj.plot([], [], lw=2)  # 15min KDJ K线
    line_d_of_15min, = ax_15min_kdj.plot([], [], lw=2)  # 15min KDJ D线
    line_j_of_15min, = ax_15min_kdj.plot([], [], lw=2)  # 15min KDJ J线

    line_k_of_60min, = ax_60min_kdj.plot([], [], lw=2)  # 60min KDJ K线
    line_d_of_60min, = ax_60min_kdj.plot([], [], lw=2)  # 60min KDJ D线
    line_j_of_60min, = ax_60min_kdj.plot([], [], lw=2)  # 60min KDJ J线

    client = ApiClient()

    symbol = Symbol(Symbol.BTC, Symbol.USDT).get_symbol()

    xs_of_1min = []
    ks_of_1min = []
    ds_of_1min = []
    js_of_1min = []

    xs_of_15min = []
    ks_of_15min = []
    ds_of_15min = []
    js_of_15min = []

    xs_of_60min = []
    ks_of_60min = []
    ds_of_60min = []
    js_of_60min = []

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=1000, interval=1000)

    plt.legend(('K', 'D', 'J'))
    plt.grid(True)
    plt.show()
