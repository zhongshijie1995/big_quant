import pandas as pd

from strategy import strategy_simple

if __name__ == '__main__':
    # code = 'AU2409'
    # while True:
    #     s = data_loader.SinaLoader().get_realtime(code)
    #     strategy_simple.MACD().add_row(s)

    data = {
        '最新价': [100, 101, 102, 103, 104, 105, 106, 107, 108, 107, 106, 105, 104, 103, 102, 101]  # 假设这里有一个价格下跌的趋势
    }
    df = pd.DataFrame(data)
    buy_chance, sell_chance = strategy_simple.MACD().get_golden_death_cross(df)
    print('做多')
    print(buy_chance)
    print('做空')
    print(sell_chance)
