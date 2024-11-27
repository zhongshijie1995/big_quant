import efinance as ef
import pandas as pd


def pick_main_contract():
    data = ef.futures.get_realtime_quotes()
    df1 = data[
        (data['期货名称'].str.contains('主')) &
        (~ data['期货名称'].str.contains('次')) &
        (data['涨跌幅'] != '-')
        ]
    df2 = data[
        (~ data['期货名称'].str.contains('主')) &
        (~ data['期货名称'].str.contains('次')) &
        (~ data['期货名称'].str.contains('连续'))
        ]
    same_cols = ['最新价', '成交量', '成交额']
    df = pd.merge(df1[same_cols], df2[['期货名称', '行情ID', '市场类型'] + same_cols], on=same_cols, how='left')
    df = df[['行情ID', '市场类型', '期货名称']]
    result = []
    for row in df.itertuples():
        if row[2] in ['大商所', '广期所', '上海能源期货交易所', '上期所', '郑商所']:
            result.append(row[1].split('.')[1])
        if row[2] in ['中金所']:
            result.append(row[3])
    with open('_data/main_contract.list', 'w') as f:
        f.write(str(result))
    return result