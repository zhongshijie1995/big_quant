from load import data_loader

if __name__ == '__main__':
    # code = 'RM2409'
    # s = data_loader.SinaLoader().get_today_min_line(code)
    # buy_chance, sell_chance = strategy_simple.MACD().get_golden_death_cross(s)
    # print('做多')
    # print(buy_chance)
    # print('做空')
    # print(sell_chance)

    codes = ['SA2409', 'RM2409', 'CS2409']
    for code in codes:
        data_loader.SinaLoader().save_line_to_csv(data_loader.SinaLoader().today_min_line, code)
