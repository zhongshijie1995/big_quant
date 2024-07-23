from typing import Dict

import pandas as pd


class MACD:
    def __init__(self, short_period, long_period, signal_period):
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period
        self.df = None

    def add_row(self, row: Dict) -> None:
        if self.df is None:
            self.df = pd.DataFrame(row)
        else:
            self.df = self.df.append(pd.DataFrame(row))

    def get_df(self) -> pd.DataFrame:
        return self.df
