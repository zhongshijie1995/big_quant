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

    def get_df(self, df_key: str):
        return self.df_dict.get(df_key)

    # short_period, long_period, signal_period
