import traceback
from typing import List

from ctpbee import CtpbeeApi
from ctpbee.constant import ContractData, TickData
from loguru import logger

from ctp import ctp_books
from ctp import ctp_tools
from indicator import indicator_prices


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

    def on_tick(self, tick: TickData) -> None:
        try:
            # 解析Tick数据
            data = ctp_tools.CtpTools().parse_tick(tick)
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
        except Exception as e:
            logger.error(f'{e}-[{traceback.format_exc()}]')


class MacdCross(ParseTickBase):

    def on_realtime(self):
        # 对账本的所有数据逐个进行监控
        for key in ctp_books.CtpBooks().keys():
            prices = [x['最新价'] for x in ctp_books.CtpBooks().query(key) if str(x['时间']).endswith('00.0')]
            if len(prices) == 0:
                continue
            macd_cross_result = indicator_prices.IndicatorPrices().macd_cross(prices)
            reports = [k for k, v in macd_cross_result.items() if v]
            if len(reports) > 0:
                logger.info(f'{key}: {reports}')
