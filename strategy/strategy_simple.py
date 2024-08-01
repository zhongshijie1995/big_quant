import copy
from typing import Dict

import pandas as pd

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class MACD:
    def __init__(self):
        self.df_dict = {}

    def add_row(self, row: Dict, max_history: int = 100) -> None:
        # 添加一条数据
        df_key = row.get('代码')
        # 将该条数据转换为Pandas
        tmp = pd.DataFrame([row])
        # 将该条数据的Pandas插入到字典中
        if df_key not in self.df_dict:
            self.df_dict[df_key] = tmp
        else:
            if self.df_dict[df_key].iloc[-1]['时间'] < row.get('时间'):
                self.df_dict[df_key] = pd.concat([self.df_dict[df_key], tmp])
        # 遗忘300条以上的K线
        if len(self.df_dict[df_key]) > max_history:
            self.df_dict[df_key] = self.df_dict[df_key].iloc[-max_history:]
        # 结束
        return None

    def update_df(self, df: pd.DataFrame) -> None:
        # 添加一条数据
        df_key = df.loc[0]['代码']
        self.df_dict[df_key] = df.copy()
        return None

    def get_df(self, df_key: str):
        return self.df_dict.get(df_key)

    @staticmethod
    def get_golden_death_cross(x, short_period=12, long_period=26) -> [pd.DataFrame, pd.DataFrame]:
        def calc_ema(xx, col, span):
            xx['%s_EMA_%s' % (col, span)] = xx[col].ewm(span=span, adjust=False).mean()

        # 拷贝数据集
        df = copy.deepcopy(x)
        # 计算
        calc_ema(df, '最新价', short_period)
        calc_ema(df, '最新价', long_period)

        # 金叉逻辑
        df['golden_cross'] = (
                (df['%s_EMA_%s' % ('最新价', short_period)] > df['%s_EMA_%s' % ('最新价', long_period)])
                &
                (df['%s_EMA_%s' % ('最新价', short_period)].shift(1) <= df['%s_EMA_%s' % ('最新价', long_period)].shift(
                    1))
        )
        # 死叉逻辑
        df['death_cross'] = (
                (df['%s_EMA_%s' % ('最新价', short_period)] < df['%s_EMA_%s' % ('最新价', long_period)])
                &
                (df['%s_EMA_%s' % ('最新价', short_period)].shift(1) >= df['%s_EMA_%s' % ('最新价', long_period)].shift(
                    1))
        )

        return df[df['golden_cross']], df[df['death_cross']]
