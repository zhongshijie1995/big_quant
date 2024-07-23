from data import data_loader
from strategy import strategy_simple

if __name__ == '__main__':
    s = data_loader.SinaLoader().get_realtime('AU2409')
    macd = strategy_simple.MACD(12, 26, 9)
    macd.add_row(s)
    macd.add_row(s)
    print(macd.get_df())
