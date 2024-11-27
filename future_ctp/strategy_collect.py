import os.path
import traceback

from ctpbee import CtpbeeApi
from ctpbee.constant import ContractData, TickData
from loguru import logger

from future_ctp import ctp_tools, ctp_record, contract_pick


class StrategiesCollect(CtpbeeApi):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        # 获取所有主力合约
        if not os.path.exists('_data/main_contract.list'):
            contract_pick.pick_main_contract()
        with open('_data/main_contract.list') as f:
            self.contracts = eval(f.read())
        logger.info(f'订阅合约[{len(self.contracts)}]个')
        # 初始化数据库
        ctp_record.ToolRecord().init_sqlite()

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
