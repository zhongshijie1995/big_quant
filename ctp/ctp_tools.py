import traceback
from typing import Dict, Any, Union

from ctpbee.constant import TickData, BarData, OrderData, TradeData, PositionData, ContractData
from loguru import logger

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class CtpTools:
    constants = {
        'TickData': {
            'ask_price_1': '卖一价',
            'ask_price_2': '卖二价',
            'ask_price_3': '卖三价',
            'ask_price_4': '卖四价',
            'ask_price_5': '卖五价',
            'ask_volume_1': '卖一量',
            'ask_volume_2': '卖二量',
            'ask_volume_3': '卖三量',
            'ask_volume_4': '卖四量',
            'ask_volume_5': '卖五量',
            'average_price': '均价',
            'bid_price_1': '买一价',
            'bid_price_2': '买二价',
            'bid_price_3': '买三价',
            'bid_price_4': '买四价',
            'bid_price_5': '买五价',
            'bid_volume_1': '买一量',
            'bid_volume_2': '买二量',
            'bid_volume_3': '买三量',
            'bid_volume_4': '买四量',
            'bid_volume_5': '买五量',
            'high_price': '最高价',
            'last_price': '最新价',
            'turnover': '成交金额',
            'limit_down': '涨停',
            'limit_up': '跌停',
            'low_price': '最低价',
            'name': '中文名',
            'open_interest': '持仓量',
            'open_price': '开盘价',
            'pre_close': '昨收盘价',
            'pre_settlement_price': '昨结算价',
            'volume': '成交量',
            'pre_open_interest': '昨持仓量',
        },
        'BarData': {
            'close_price': '收盘价',
            'high_price': '最高价',
            'interval': '周期间隔',
            'low_price': '最低价',
            'open_price': '开盘价格',
            'volume': 'k线内成交量',
        },
        'OrderData': {
            'volume': '发单量',
            'direction': '买卖方向',
            'local_order_id': '本地发单id',
            'offset': '开平',
            'price': '价格',
            'status': '状态',
            'time': '时间',
            'traded': '是否已经成交',
            'type': '价格类型',
        },
        'TradeData': {
            'direction': '买卖方向',
            'local_order_id': '本地发单id',
            'local_trade_id': '本地成交id',
            'offset': '开平',
            'price': '价格',
            'time': '时间',
            'volume': '成交量',
        },
        'PositionData': {
            'frozen': '冻结',
            'local_position_id': '持仓id',
            'pnl': '结算盈亏',
            'price': '价格',
            'volume': '持仓总量',
            'yd_volume': '昨日持仓量',
            'open_price': '仓位持仓成本',
            'float_pnl': '浮动盈亏',
        },
        'AccountData': {
            'balance': '余额',
            'frozen': '冻结',
            'local_account_id': '本地账户id',
            'available': '可用资金',
        },
        'ContractData': {
            'min_volume': '最小交易量（推测含义）',
            'net_position': '净头寸（推测含义）',
            'option_expiry': '到期日',
            'option_strike': '执行价',
            'option_type': '期权类型',
            'option_underlying': '基础商品代码',
            'stop_supported': '停止支持（推测含义）',
            'pricetick': '最小变动价位',
            'product': '产品类型',
            'size': '合约乘数',
            'name': '合约名称',
            'exchange': '交易所',
        },
    }

    @staticmethod
    def obj_attr_val_to_dict_key_val(p_obj: Any, p_dict: Dict, attr_name: str, key_name: str) -> Dict:
        try:
            p_dict[key_name] = eval(f'target_obj.{attr_name}')
        except:
            logger.error(traceback.format_exc())
            p_dict[key_name] = None
        return p_dict

    @staticmethod
    def obj_to_dict(p_obj: Union[TickData, BarData, OrderData, TradeData, PositionData, ContractData]) -> Dict:
        maps = CtpTools().constants[type(p_obj).__name__]
        result = {}
        for k, v in maps.items():
            CtpTools().obj_attr_val_to_dict_key_val(p_obj, result, k, v)
        return result
