import traceback

import efinance as ef
import pandas as pd
from ctpbee import CtpbeeApi
from ctpbee.constant import ContractData, TickData
from loguru import logger

from future_ctp import ctp_tools, ctp_record


class StrategiesCollect(CtpbeeApi):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        # 获取所有主力合约
        self.contracts = self.pick_main_contract()
        # 初始化数据库
        ctp_record.ToolRecord().init_sqlite()
        # 归档昨日数据
        ctp_record.ToolRecord().export_and_clear_yesterday_from_sqlite()

    @staticmethod
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
        return result

    def on_contract(self, contract: ContractData) -> None:
        if contract.symbol in self.contracts:
            logger.info(f'订阅[{contract.symbol}]')
            self.action.subscribe(contract.local_symbol)

    def on_tick(self, tick: TickData) -> None:
        try:
            # 解析Tick数据
            data = ctp_tools.CtpTools().parse_tick(tick)
            if data is None:
                logger.info('未开盘...')
                return None
        except Exception as e:
            logger.error(f'{e}-[{traceback.format_exc()}]')

    def on_realtime(self) -> None:
        pass
