import tkinter as tk
import traceback
from datetime import datetime
from tkinter import ttk
from typing import List

from ctpbee import CtpbeeApi
from future_ctp import indicator_prices, ctp_tools, ctp_books
from ctpbee.constant import ContractData, TickData
from loguru import logger

from comm.tool_record import ToolRecord


class StrategiesMacd(CtpbeeApi):
    def __init__(self, contracts: List[str], with_tkinter: bool = False):
        super().__init__(self.__class__.__name__)
        # 初始化数据库
        ToolRecord().init_sqlite()
        # 接收合约
        if contracts is None:
            contracts = []
        self.instrument_set = contracts
        # 是否需要界面
        self.with_tkinter = with_tkinter
        # 完成界面
        if with_tkinter:
            # 创建界面
            self.tkinter_root = tk.Tk()
            self.tkinter_root.title('big_quant')
            # 为界面准备UI
            self.widgets = {}
            # 添加时间栏
            datetime_frame = '日期时间'
            self.widgets[datetime_frame] = tk.Label(self.tkinter_root, text='日期时间')
            self.widgets[datetime_frame].pack(side=tk.TOP, fill=tk.X)
            # 添加合约
            notebook = 'contract_notebook'
            self.widgets[notebook] = ttk.Notebook(self.tkinter_root)
            for contract in contracts:
                # ------------ 创建页面 ------------
                tab = f'contract_frame.{contract}'
                self.widgets[tab] = tk.Frame(self.widgets[notebook])
                # 现价
                f_price = 'contract_price_frame'
                self.widgets[f'{f_price}.{contract}'] = tk.Label(self.widgets[tab], text='现价')
                self.widgets[f'{f_price}.{contract}'].pack(side=tk.TOP, fill=tk.X)
                # 盘口
                f_position = 'contract_position_frame'
                self.widgets[f_position] = tk.Frame(self.widgets[tab])
                self.widgets[f'{f_position}.{contract}.买1'] = tk.Label(self.widgets[f_position], text='买1')
                self.widgets[f'{f_position}.{contract}.买1'].pack(side=tk.LEFT)
                self.widgets[f'{f_position}.{contract}.卖1'] = tk.Label(self.widgets[f_position], text='卖1')
                self.widgets[f'{f_position}.{contract}.卖1'].pack(side=tk.RIGHT)
                self.widgets[f'{f_position}'].pack(side=tk.TOP, fill=tk.X)
                # 明细
                f_detail = 'contract_detail_frame'
                self.widgets[f_detail] = tk.Frame(self.widgets[tab])
                # 明细-汇总
                self.widgets[f'{f_detail}.{contract}.汇总'] = tk.Label(self.widgets[tab], text='汇总')
                self.widgets[f'{f_detail}.{contract}.汇总'].pack(side=tk.TOP, fill=tk.X)
                # 明细-成交
                self.widgets[f'{f_detail}.{contract}.多'] = tk.Text(self.widgets[f_detail], width=17, height=10)
                self.widgets[f'{f_detail}.{contract}.多'].pack(side=tk.LEFT, fill=tk.X)
                self.widgets[f'{f_detail}.{contract}.空'] = tk.Text(self.widgets[f_detail], width=17, height=10)
                self.widgets[f'{f_detail}.{contract}.空'].pack(side=tk.RIGHT, fill=tk.X)
                self.widgets[f'{f_detail}'].pack(side=tk.TOP, fill=tk.X)
                # 策略提示
                strategy_frame = 'contract_strategy_frame'
                self.widgets[f'{strategy_frame}.{contract}'] = tk.Text(self.widgets[tab], width=35, height=10)
                self.widgets[f'{strategy_frame}.{contract}'].pack(side=tk.BOTTOM, fill=tk.X)
                # ------------ 载入页面 ------------
                self.widgets[notebook].add(self.widgets[tab], text=contract)
            self.widgets[notebook].pack(side=tk.BOTTOM, fill=tk.X)

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
            if data is None:
                logger.info('未开盘...')
                return None
            # 打印报价
            price_msg = ctp_books.CtpBooks().query(data['代码'], -1)[0]
            msg = {
                '品种名': price_msg.get('品种名'),
                '买1': f'{price_msg["买价1"]}  ->  {price_msg["买量1"]}',
                '卖1': f'{price_msg["卖量1"]}  <-  {price_msg["卖价1"]}',
                '最新价': price_msg.get('最新价'),
                '明细': price_msg.get('明细'),
            }
            logger.info(msg)
            self.update_price(data["代码"], msg.get('最新价'))
            self.update_position(data["代码"], msg.get('买1'), msg.get('卖1'))
            self.update_detail(data["代码"], msg.get('明细'))
        except Exception as e:
            logger.error(f'{e}-[{traceback.format_exc()}]')

    def on_realtime(self):
        # 每秒更新一次日期时间
        now_datetime = self.update_datetime()
        # 每日盘前
        if now_datetime.endswith('20:50:00'):
            for contract in self.instrument_set:
                text_key = f'contract_detail_frame.{contract}'
                self.clear_text(text_key)
                text_key = f'contract_strategy_frame.{contract}'
                self.clear_text(text_key)
        # 每分钟
        if now_datetime.endswith('00'):
            # 对账本的所有数据逐个进行监控，报出MACD策略
            for key in ctp_books.CtpBooks().keys():
                prices = [x['最新价'] for x in ctp_books.CtpBooks().query(key) if str(x['时间']).endswith('00.0')]
                if len(prices) == 0:
                    continue
                macd_cross_result = indicator_prices.IndicatorPrices().macd_cross(prices)
                reports = [k for k, v in macd_cross_result.items() if v]
                if len(reports) == 0:
                    continue
                self.update_strategy(key, f'{now_datetime}-{reports[-1]}')
                logger.info(f'{key}: {reports}')

    def update_datetime(self):
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.widgets['日期时间'].config(text=now_datetime)
        self.tkinter_root.update()
        return now_datetime

    def update_price(self, contract: str, price: str):
        text_key = f'contract_price_frame.{contract}'
        self.widgets[text_key].config(text=price)

    def update_position(self, contract: str, buy: str, sell: str):
        text_key = f'contract_position_frame.{contract}.买1'
        self.widgets[text_key].config(text=buy)
        text_key = f'contract_position_frame.{contract}.卖1'
        self.widgets[text_key].config(text=sell)
        self.tkinter_root.update()

    def update_detail(self, contract: str, detail: str):
        if detail is None:
            detail = ''
        if '↑' not in detail and '↓' not in detail:
            return
        detail_type = {'↑': '多', '↓': '空'}.get(detail.split('-')[1])
        text_key = f'contract_detail_frame.{contract}.{detail_type}'
        # 明细-汇总
        x = ctp_books.CtpBooks().get_detail(contract)
        detail_submit_str = '\n'.join([f'【{k}】{v}' for k, v in {
            '多开': x['多开'],
            '空平': x['空平'],
            '日内新多': x['多开'] - x['多平'],
            '日内新空': x['空开'] - x['空平'],
            '多平': x['多平'],
            '空开': x['空开'],
        }.items()])
        self.widgets[f'contract_detail_frame.{contract}.汇总'].config(text=detail_submit_str)
        # 明细-成交
        self.widgets[text_key].insert(tk.END, f'{detail}\n')
        self.widgets[text_key].see(tk.END)
        self.tkinter_root.update()

    def update_strategy(self, contract: str, strategy: str):
        if strategy is None:
            strategy = ''
        text_key = f'contract_strategy_frame.{contract}'
        self.widgets[text_key].insert(tk.END, strategy + '\n')
        self.widgets[text_key].see(tk.END)
        self.tkinter_root.update()

    def clear_text(self, clear_text_key: str):
        self.widgets[clear_text_key].delete('1.0', tk.END)
        self.tkinter_root.update()
