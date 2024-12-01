import efinance as ef
import pandas as pd

def collect_future_day_history():
    # 1.收集行情ID
    base_info = ef.futures.get_futures_base_info()
    cod_list = set(base_info[(base_info['期货名称'].str.contains('主')) &  (~base_info['期货名称'].str.contains('次'))]['行情ID'])

    # 2.收集历史
    history_dict = ef.futures.get_quote_history(cod_list)

    # 3. 合并历史
    result = pd.concat(history_dict.values())
    return result


def split_train_test():
    pass


history_dict = collect_future_day_history()
