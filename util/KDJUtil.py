# coding:utf-8
from policy.KDJ import KDJ


def kdj(ticks, period):
    '''
    :param ticks: 离散点数据
    :param period: KDJ随机指标值计算周期，即用前period个离散点来计算当前点的KDJ信息
    :return: tick列表与tick对应的kdj信息列表
    '''
    size = len(ticks)
    if size <= 0 or size < period:  # 离散点为空,或者离散点数量小于随机指标计算周期
        print "Error: ticks size < 0 or size < period"
        return None

    if size == period:
        return [ticks[-1]], [KDJ(ticks)]

    kdjs = []
    ts = []

    for i in range(0, size - period):
        data = ticks[i: i + period]

        _kdj = KDJ(data)

        kdjs.append(_kdj)
        ts.append(data[-1])
    return ts, kdjs
