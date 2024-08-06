import pandas as pd
from loguru import logger

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class Trader:
    def __init__(self):
        self.wallet = 10000
        self.trace = pd.DataFrame()
        # self.trace.columns = ['日期', '时间', '代码', '名称', '价格', '手数', '方向']

    @staticmethod
    def clac_amt(price: float, price_rate: float, num: int) -> float:
        return price * price_rate * num

    def check_wallet(self, cost: float) -> bool:
        return self.wallet >= cost

    def use_wallet(self, cost: float) -> None:
        self.wallet -= cost
        return None

    def show_wallet(self) -> None:
        logger.info(f'钱包余额{self.wallet}')
        return None

    def call(self, code: str, price: float, num: int) -> None:
        # 计算支出
        price_rate = 1
        amt = Trader().clac_amt(price, price_rate, num)
        # 检查钱包是否足够
        if not self.check_wallet(amt):
            logger.info('购买失败')
        # 使用钱包
        self.use_wallet(amt)
        # 展示余额
        self.show_wallet()

    def close_call(self, code: str, price: float, num: int):
        # 计算收入
        price_rate = 1
        amt = Trader().clac_amt(price, price_rate, num)
        amt = - amt
        # 使得钱包生效
        self.use_wallet(amt)
        # 展示余额
        self.show_wallet()

    def put(self):
        pass

    def close_put(self):
        pass


if __name__ == '__main__':
    Trader().call('XXX', 2300, 1)
    Trader().close_call('XXX', 2500, 1)
