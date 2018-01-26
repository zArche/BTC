# coding:utf-8

import MySQLdb


class TickDao:

    def __init__(self, host_name, user_name, password, database_name):
        self.db = MySQLdb.connect(host_name, user_name, password, database_name)
        self.cursor = self.db.cursor()

    def insert(self, table, ticks):
        values = ""
        for tick in ticks:
            values = values + "(%s,%s,%s,%s,%s,%s,%s,%s)," % (
                tick.id, tick.count, tick.vol, tick.high, tick.amount, tick.low, tick.close, tick.open)

        values = values[0:-1]

        sql = """INSERT INTO %s(tick_id,count, vol, high, amount,low,close,open)
                 VALUES %s""" % (table, values)

        print sql

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def close(self):
        self.db.close()
