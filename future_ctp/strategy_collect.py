from ctpbee import CtpbeeApi
from ctpbee.constant import ContractData
from loguru import logger

from future_ctp import ctp_tools


class StrategiesCollect(CtpbeeApi):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    def on_contract(self, contract: ContractData) -> None:
        data = ctp_tools.CtpTools().obj_to_dict(contract)
        logger.info(f'contract: {data}')
