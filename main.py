import time

from data import data_loader
from strategy import strategy_simple

if __name__ == '__main__':
    code = 'AU2409'
    while True:
        s = data_loader.SinaLoader().get_realtime(code)
        strategy_simple.MACD().add_row(s)
        time.sleep(1)
