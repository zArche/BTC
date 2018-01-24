# coding:utf-8
from model.Object import Object


class Symbol(Object):
    BTC = "btc"
    BCH = "bch"
    XRP = "xrp"
    ETH = "eth"
    LTC = "ltc"
    DASH = "dash"
    EOS = "eos"
    ETC = "etc"
    OMG = "omg"
    ZEC = "zec"
    USDT = "usdt"

    """
    交易对
    """

    def __init__(self, base_currency, quote_currency):
        '''
        :param base_currency:基础币种
        :param quote_currency:计价币种
        '''
        self.base_currency = base_currency
        self.quote_currency = quote_currency

    def get_symbol(self):
        return self.base_currency + self.quote_currency
