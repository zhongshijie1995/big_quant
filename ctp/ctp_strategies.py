from typing import List

from ctpbee import CtpbeeApi
from ctpbee.constant import ContractData, TickData
from loguru import logger

from ctp import ctp_tools


class LogTick(CtpbeeApi):
    def __init__(self, contracts: List[str] = None):
        super().__init__(self.__class__.__name__)
        if contracts is None:
            contracts = []
        self.instrument_set = contracts

    def on_contract(self, contract: ContractData):
        if contract.local_symbol in self.instrument_set:
            self.action.subscribe(contract.local_symbol)

    def on_tick(self, tick: TickData) -> None:
        data = ctp_tools.CtpTools().obj_to_dict(tick)
        data = {k: v for k, v in data.items() if v is not None}
        logger.info(f'{data}')
        logger.info(f'{ctp_tools.CtpTools().obj_to_dict(tick)}')


class MacdCross(CtpbeeApi):
    def __init__(self, contracts: List[str] = None):
        super().__init__(self.__class__.__name__)
        if contracts is None:
            contracts = []
        self.instrument_set = contracts

    def on_contract(self, contract: ContractData):
        if contract.local_symbol in self.instrument_set:
            self.action.subscribe(contract.local_symbol)

    def on_tick(self, tick: TickData):
        pass
