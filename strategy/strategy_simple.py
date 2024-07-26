import copy
from typing import Dict

import pandas as pd

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class MACD:
    def __init__(self):
        self.df_dict = {}

    def add_row(self, row: Dict) -> None:
        # 添加一条数据
        df_key = row.get('代码')
        if df_key not in self.df_dict:
            self.df_dict[df_key] = pd.DataFrame([row])
        else:
            self.df_dict[df_key] = self.df_dict[df_key]._append(row, ignore_index=True)
        MACD().get_golden_cross(self.df_dict[df_key])

    def get_df(self, df_key: str):
        return self.df_dict.get(df_key)

    @staticmethod
    def get_golden_cross(df, short_period=12, long_period=26, signal_period=9):
        def calc_ema(x, col, span):
            x['%s_EMA_%s' % (col, span)] = x[col].ewm(span=span, adjust=False).mean()

        tmp = copy.deepcopy(df)
        calc_ema(tmp, '最新价', short_period)
        calc_ema(tmp, '最新价', long_period)
        tmp['DIF'] = tmp['%s_EMA_%s' % ('最新价', short_period)] - tmp['%s_EMA_%s' % ('最新价', long_period)]
        calc_ema(tmp, 'DIF', signal_period)
        tmp['DEA'] = tmp['%s_EMA_%s' % ('DIF', signal_period)]
        tmp['MACD'] = tmp['DIF'] - tmp['DEA']
        tmp['golden_cross'] = (tmp['DIF'] < tmp['DEA'].shift(1)) & (tmp['DIF'].shift(-1) > tmp['DEA'].shift(-1))
        if tmp.iloc[-1]['golden_cross'].tolist():
            print(tmp.iloc[-1])
