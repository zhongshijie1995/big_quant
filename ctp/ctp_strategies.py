from typing import List, Dict

from ctpbee import CtpbeeApi
from ctpbee.constant import ContractData, TickData
from loguru import logger

from comm import tool_record
from ctp import ctp_tools


class ParseTickBase(CtpbeeApi):
    class TicksBook:
        book = {}

    def __init__(self, contracts: List[str] = None):
        super().__init__(self.__class__.__name__)
        if contracts is None:
            contracts = []
        self.instrument_set = contracts
        self.tmp_tick_dict = {}

    def on_contract(self, contract: ContractData):
        data = ctp_tools.CtpTools().obj_to_dict(contract)
        contract_name = data.get('合约名称')
        if contract_name in self.instrument_set:
            logger.info(f'订阅[{contract_name}]-[{contract.local_symbol}]')
            self.action.subscribe(contract.local_symbol)

    def parse_tick(self, tick: TickData) -> Dict:
        data = ctp_tools.CtpTools().obj_to_dict(tick)
        data = {k: v for k, v in data.items() if v is not None}
        the_code = data['代码']
        if the_code in self.tmp_tick_dict:
            detail = ctp_tools.CtpTools().parse_detail(self.tmp_tick_dict[the_code], data.copy())
            data['明细'] = detail['汇总']
        self.tmp_tick_dict[the_code] = data
        return data

    def on_tick(self, tick: TickData) -> None:
        # 解析Tick数据
        data = self.parse_tick(tick)
        # 记录历史文件
        tool_record.ToolRecord().append_to_date_file(str(data))
        # 打印日志
        logger.info(data)
