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
            if self.df_dict[df_key].iloc[-1]['时间'] != row.get('时间'):
                self.df_dict[df_key] = pd.concat([self.df_dict[df_key], pd.DataFrame([row])])

    def get_df(self, df_key: str):
        return self.df_dict.get(df_key)

    @staticmethod
    def get_golden_cross(x, short_period=12, long_period=26, signal_period=9):
        def calc_ema(xx, col, span):
            xx['%s_EMA_%s' % (col, span)] = xx[col].ewm(span=span, adjust=False).mean()

        df = copy.deepcopy(x)
        # 直接在原DataFrame上操作
        calc_ema(df, '最新价', short_period)
        calc_ema(df, '最新价', long_period)
        df['DIF'] = df['%s_EMA_%s' % ('最新价', short_period)] - df['%s_EMA_%s' % ('最新价', long_period)]
        calc_ema(df, 'DIF', signal_period)
        df['DEA'] = df['%s_EMA_%s' % ('DIF', signal_period)]
        df['MACD'] = df['DIF'] - df['DEA']

        # 金叉逻辑
        df['golden_cross'] = (df['%s_EMA_%s' % ('最新价', short_period)] > df['%s_EMA_%s' % ('最新价', long_period)]
                              ) & (df['%s_EMA_%s' % ('最新价', short_period)].shift(1) <= df[
            '%s_EMA_%s' % ('最新价', long_period)].shift(1))
        # 死叉逻辑
        df['death_cross'] = ((df['%s_EMA_%s' % ('最新价', short_period)] < df['%s_EMA_%s' % ('最新价', long_period)]) &
                             (df['%s_EMA_%s' % ('最新价', short_period)].shift(1) >= df[
                                 '%s_EMA_%s' % ('最新价', long_period)].shift(1)))

        print([df.iloc[-1]['时间'], df.iloc[-1]['golden_cross'], df.iloc[-1]['death_cross']])

        # # 如果最后一行是黄金交叉，则打印
        # if df.iloc[-1]['golden_cross'] and df.iloc[-1]['death_cross']:
        #     print(df.iloc[-1])
