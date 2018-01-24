# coding:utf-8
from model.Object import Object


class Account(Object):
    def __init__(self, id, state, type, subtype):
        '''
        :param id:账户id
        :param state:账户状态 working:正常 lock:锁定
        :param type:账户类型 spot:现货账户
        :param subtype:子类型
        '''

        self.id = id
        self.state = state
        self.type = type
        self.subtype = subtype
