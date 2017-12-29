import time
import requests


class MarketPoller(object):
    def __init__(self, market, frequency=5):
        self. market = market
        self.frequency = frequency

    def run(self):
        response = requests.get("https://bittrex.com/api/v1.1/public/getticker", params={"market": market})
        coin_data = response.json()

        bid_price = coin_data['result']['Ask']
        time.sleep(self.frequency)
