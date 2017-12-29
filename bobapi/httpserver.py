import tornado.web
from bittrex.bittrex import Bittrex
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


class DataStore(object):
    def __init__(self):
        self.api_key = None
        self.api_secret = None
        self.bittrex_api = None

    def set_values(self, api_key, api_secret, bittrex_api):
        self.api_key = api_key
        self.api_secret = api_secret
        self.bittrex_api = bittrex_api


class BittrexApiHandler(tornado.web.RequestHandler):
    def initialize(self, data):
        super(BittrexApiHandler, self).initialize()
        self.data = data


class MainHandler(BittrexApiHandler):
    def get(self):
        self.write("Hello, world {}".format(self.data.api_key))


class LoginHandler(BittrexApiHandler):
    def get(self):
        api_key = self.get_argument("api_key")
        api_secret = self.get_argument("api_secret")
        if api_key and api_secret:
            bittrex_api = Bittrex(api_key, api_secret)
            self.data.set_values(api_key, api_secret, bittrex_api)
            self.redirect("/")
        else:
            self.write("Please enter api key and api secret")


class BuyLimitHandler(BittrexApiHandler):
    def get(self):
        bittrex_api = Bittrex(None, None)
        market = self.get_argument("market")
        quantity = self.get_argument("quantity")
        rate = self.get_argument("rate")
        bittrex_api.buy_limit(market, quantity, rate)
        # TODO: actually check if action successfully done
        self.write("{market} {quantity} {rate}".format(market=market, quantity=quantity, rate=rate))


class SellLimitHandler(BittrexApiHandler):
    def get(self):
        bittrex_api = Bittrex(None, None)
        market = self.get_argument("market")
        quantity = self.get_argument("quantity")
        rate = self.get_argument("rate")
        bittrex_api.sell_limit(market, quantity, rate)
        # TODO: actually check if action successfully done
        self.write("{market} {quantity} {rate}".format(market=market, quantity=quantity, rate=rate))


def make_app():
    data_db = DataStore()
    return tornado.web.Application([
        (r"/", MainHandler, dict(data=data_db)),
        (r"/login", LoginHandler, dict(data=data_db)),
        (r"/buy", BuyLimitHandler, dict(data=data_db)),
        (r"/sell", SellLimitHandler, dict(data=data_db))
    ])


if __name__ == "__main__":
    app = make_app()
    server = HTTPServer(app)
    server.listen(8888)
    IOLoop.current().start()
