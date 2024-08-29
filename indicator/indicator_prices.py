from typing import List, Dict

import pandas as pd

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class IndicatorPrices:
    @staticmethod
    def macd_cross(prices: List[float], short_window=12, long_window=26, signal_window=9) -> Dict[str, bool]:
        def calculate_macd():
            exp1 = df['close'].rolling(window=short_window, min_periods=1).mean()
            exp2 = df['close'].rolling(window=long_window, min_periods=1).mean()
            df['DIF'] = exp1 - exp2
            df['DEA'] = df['DIF'].rolling(window=signal_window, min_periods=1).mean()

        def find_crossovers():
            df['金叉'] = ((df['DIF'].shift(1) < df['DEA'].shift(1)) & (df['DIF'] >= df['DEA']))
            df['死叉'] = ((df['DIF'].shift(1) > df['DEA'].shift(1)) & (df['DIF'] <= df['DEA']))

        df = pd.DataFrame(prices, columns=['close'])
        calculate_macd()
        find_crossovers()
        result = df[['金叉', '死叉']].iloc[-1].to_dict()
        return result
