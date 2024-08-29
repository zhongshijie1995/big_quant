from typing import List, Dict

from ctpbee import CtpbeeApi
from ctpbee.constant import ContractData, TickData
from loguru import logger

from ctp import ctp_books
from ctp import ctp_tools


class ParseTickBase(CtpbeeApi):
    def __init__(self, contracts: List[str] = None):
        super().__init__(self.__class__.__name__)
        if contracts is None:
            contracts = []
        self.instrument_set = contracts

    def on_contract(self, contract: ContractData):
        data = ctp_tools.CtpTools().obj_to_dict(contract)
        contract_name = data.get('合约名称')
        if contract_name in self.instrument_set:
            logger.info(f'订阅[{contract_name}]-[{contract.local_symbol}]')
            self.action.subscribe(contract.local_symbol)

    def parse_tick(self, tick: TickData) -> Dict:
        data = ctp_tools.CtpTools().obj_to_dict(tick)
        data = {k: v for k, v in data.items() if v is not None}
        ctp_books.CtpBooks().append(data['代码'], data)
        return data

    def on_tick(self, tick: TickData) -> None:
        # 解析Tick数据
        data = self.parse_tick(tick)
        # 打印报价
        price_msg = ctp_books.CtpBooks().query(data['代码'], -1)[0]
        msg = {
            '品种名': price_msg.get('品种名'),
            '买1': f'{price_msg["买价1"]}:{price_msg["买量1"]}',
            '卖1': f'{price_msg["卖价1"]}:{price_msg["卖量1"]}',
            '最新价': price_msg.get('最新价'),
            '明细': price_msg.get('明细'),
        }
        logger.info(msg)
