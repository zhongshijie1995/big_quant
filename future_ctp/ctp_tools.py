import traceback
from typing import Dict, Any, Union

from ctpbee.constant import TickData, BarData, OrderData, TradeData, PositionData, ContractData
from loguru import logger

from comm import tool_classes
from future_ctp import ctp_books


@tool_classes.ToolClasses.singleton
class CtpTools:
    constants = {
        'TickData': {
            'datetime': '时间',
            'symbol': '代码',
            'exchange': '交易所',
            'name': '品种名',
            'volume': '成交量',
            'last_price': '最新价',
            'last_volume': '最新量',
            'limit_up': '涨停',
            'limit_down': '跌停',
            'open_interest': '持仓量',
            'average_price': '均价',
            'settlement_price': '结算价',
            'pre_settlement_price': '昨结算价',
            'pre_open_interest': '昨持仓量',
            'open_price': '开盘价',
            'high_price': '最高价',
            'low_price': '最低价',
            'pre_close': '昨收盘价',
            'turnover': '成交金额',
            'bid_price_1': '买价1',
            'bid_price_2': '买价2',
            'bid_price_3': '买价3',
            'bid_price_4': '买价4',
            'bid_price_5': '买价5',
            'ask_price_1': '卖价1',
            'ask_price_2': '卖价2',
            'ask_price_3': '卖价3',
            'ask_price_4': '卖价4',
            'ask_price_5': '卖价5',
            'bid_volume_1': '买量1',
            'bid_volume_2': '买量2',
            'bid_volume_3': '买量3',
            'bid_volume_4': '买量4',
            'bid_volume_5': '买量5',
            'ask_volume_1': '卖量1',
            'ask_volume_2': '卖量2',
            'ask_volume_3': '卖量3',
            'ask_volume_4': '卖量4',
            'ask_volume_5': '卖量5',
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
            p_dict[key_name] = eval(f'p_obj.{attr_name}')
            if key_name == '时间':
                p_dict[key_name] = p_dict[key_name].strftime('%Y-%m-%d %H:%M:%S.%f')[:-5]
            if key_name == '交易所':
                p_dict[key_name] = p_dict[key_name].value
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

    @staticmethod
    def parse_detail(last_tick: Dict[str, Any], now_tick: Dict[str, Any]) -> Dict:
        result = {}
        result['现手'] = now_tick['成交量'] - last_tick['成交量']
        result['增仓'] = now_tick['持仓量'] - last_tick['持仓量']
        # 性质
        if result['现手'] == result['增仓'] > 0:
            result['性质'] = '双开'
        elif result['现手'] > result['增仓'] > 0:
            result['性质'] = '开仓'
        elif result['现手'] > (- result['增仓']) > 0:
            result['性质'] = '平仓'
        elif result['现手'] > result['增仓'] == 0:
            result['性质'] = '换手'
        elif result['现手'] + result['增仓'] == 0:
            result['性质'] = '双平'
        else:
            result['性质'] = '未知'
        # 方向
        if now_tick['最新价'] >= last_tick['卖价1']:
            result['方向'] = '向上'
        elif now_tick['最新价'] <= last_tick['买价1']:
            result['方向'] = '向下'
        elif now_tick['最新价'] >= now_tick['卖价1']:
            result['方向'] = '向上'
        elif now_tick['最新价'] <= now_tick['买价1']:
            result['方向'] = '向上'
        else:
            result['方向'] = '不变'
        # 汇总
        if result['性质'] == '换手' and result['方向'] == '向上':
            result['汇总'] = '多换-↑'
        elif result['性质'] == '换手' and result['方向'] == '向下':
            result['汇总'] = '空换-↓'
        elif result['性质'] == '双开' and result['方向'] == '向上':
            result['汇总'] = '双开-↑'
        elif result['性质'] == '双开' and result['方向'] == '向下':
            result['汇总'] = '双开-↓'
        elif result['性质'] == '平仓' and result['方向'] == '向上':
            result['汇总'] = '空平-↑'
        elif result['性质'] == '平仓' and result['方向'] == '向下':
            result['汇总'] = '多平-↓'
        elif result['性质'] == '开仓' and result['方向'] == '向上':
            result['汇总'] = '多开-↑'
        elif result['性质'] == '开仓' and result['方向'] == '向下':
            result['汇总'] = '空开-↓'
        elif result['性质'] == '双平' and result['方向'] == '向上':
            result['汇总'] = '双平-↑'
        elif result['性质'] == '双平' and result['方向'] == '向下':
            result['汇总'] = '双平-↓'
        else:
            result['汇总'] = '未知'
        # 整理汇总信息
        if result['汇总'] != '未知':
            result['汇总'] += f'-{result["现手"]}-{int(result["增仓"])}'
        return result

    @staticmethod
    def parse_tick(tick: TickData) -> Dict:
        data = CtpTools().obj_to_dict(tick)
        data = {k: v for k, v in data.items() if v is not None}
        ctp_books.CtpBooks().append(data['代码'], data)
        return data
