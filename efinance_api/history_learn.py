from typing import Callable

import efinance as ef
import pandas as pd

pd.set_option('display.max_columns', None)


def collect_future_day_history(deal_func: Callable):
    # 1.收集行情ID
    base_info = ef.futures.get_futures_base_info()
    cod_list = list(
        base_info[(base_info['期货名称'].str.contains('主')) & (~base_info['期货名称'].str.contains('次'))]['行情ID'])

    # 2.收集历史
    history_dict = ef.futures.get_quote_history(cod_list)

    # 2.1 处理单个历史
    for k, v in history_dict.items():
        history_dict[k] = deal_func(v)

    # 3. 合并历史
    result = pd.concat(history_dict.values())

    # 4.返回结果
    return result


def ft(df: pd.DataFrame):
    col_name = '次日涨幅'
    df[col_name] = df['收盘'] - df['收盘'].shift(1)
    df = df[df[col_name].notna()]
    return df


if __name__ == '__main__':
    data = collect_future_day_history(ft)
    print(data[['日期', '期货名称', '收盘', '次日涨幅']])
