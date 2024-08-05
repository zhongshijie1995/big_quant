import copy

import pandas as pd

from comm import tool_classes
from load import data_loader


@tool_classes.ToolClasses.singleton
class MACD:
    @staticmethod
    def golden_death_cross(data, short=12, long=26) -> pd.DataFrame:
        def calc_ema(xx, col, span):
            xx['%s_EMA_%s' % (col, span)] = xx[col].ewm(span=span, adjust=False).mean()

        # 拷贝数据集
        df = copy.deepcopy(data)
        # 计算
        calc_ema(df, '最新价', short)
        calc_ema(df, '最新价', long)

        # 金叉逻辑
        df['多'] = (
                (df['%s_EMA_%s' % ('最新价', short)] > df['%s_EMA_%s' % ('最新价', long)])
                &
                (df['%s_EMA_%s' % ('最新价', short)].shift(1) <= df['%s_EMA_%s' % ('最新价', long)].shift(1))
        )
        # 死叉逻辑
        df['空'] = (
                (df['%s_EMA_%s' % ('最新价', short)] < df['%s_EMA_%s' % ('最新价', long)])
                &
                (df['%s_EMA_%s' % ('最新价', short)].shift(1) >= df['%s_EMA_%s' % ('最新价', long)].shift(1))
        )
        # 获取名称
        df['名称'] = data_loader.SinaLoader().realtime_quote(df.loc[0]['代码'][-6:])['名称']
        # 精简数据列
        df = df[['时间', '名称', '最新价', '多', '空']]
        # 过滤有效数据
        df = df[(df['多'] | df['空'])]
        return df
