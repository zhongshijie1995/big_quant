from data import data_loader
from strategy import strategy_simple

if __name__ == '__main__':
    code = 'AU2409'
    s = data_loader.SinaLoader().get_realtime(code)
    strategy_simple.MACD().add_row(s)
    print(strategy_simple.MACD().get_df(s.get('代码')))
