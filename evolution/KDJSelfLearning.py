# coding:utf-8
from model.Object import Object


class KDJSelfLearning(Object):
    '''
    KDJ自学习进化
    算法:
        使用历史数据，对KDJ的周期因子、K线/D线因子进行测试，选出最佳值
        1.初始化因子数组
        2.遍历因子数组，带入KDJ策略算法，给出买入/卖出信号
        3.当前点价格 - 下一个点价格, 将结果与买入/卖出信号进行比对
    '''

    periods = []