# coding:utf-8

import MySQLdb


class TickDao:

    def __init__(self, host_name, user_name, password, database_name):
        self.db = MySQLdb.connect(host_name, user_name, password, database_name)
        self.cursor = self.db.cursor()

    def insert(self, table, ticks, kdjs, period):
        '''
        :param table: 表名
        :param ticks: 离散点数据
        :param kdjs: 对应的kdj数据
        :param period: 离散点时间单位(1min,15min,60min)
        :return:
        '''
        values = ""
        for i in range(0, len(ticks)):
            tick = ticks[i]
            kdj = kdjs[i]
            avg = float(tick.vol) / float(tick.amount)
            values = values + "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')," % (
                tick.id, period, tick.count, tick.vol, tick.high, tick.amount, tick.low, tick.close, tick.open, kdj.k,
                kdj.d, kdj.j, avg)

        values = values[0:-1]

        sql = """INSERT INTO %s(tick_id,period,count, vol, high, amount,low,close,open,k,d,j,avg)
                 VALUES %s""" % (table, values)

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def update(self, table, tick_id, tick, kdj, period):
        '''
         :param table: 表名
         :param tick: 离散点数据
         :param kdj: 对应的kdj数据
         :param period: 离散点时间单位(1min,15min,60min)
         :return:
         '''

        sql = """UPDATE %s SET period = %s,count = %s,vol = %s,high = %s,
        amount = %s,low = %s,close = %s,open = %s,k = %s,d = %s,j = %s""" % (
            table, period, tick.count, tick.vol, tick.high, tick.amount, tick.low, tick.close, tick.open, kdj.k, kdj.d,
            kdj.j)

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def delete(self, table, tick_id):
        sql = "DELETE FROM %s WHERE tick_id = %s" % (table, tick_id)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def close(self):
        self.db.close()
