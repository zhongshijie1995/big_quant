import tkinter as tk
import traceback
from datetime import datetime
from tkinter import ttk
from typing import List

from ctpbee import CtpbeeApi
from ctpbee.constant import ContractData, TickData
from loguru import logger

from ctp import ctp_tools, ctp_books
from indicator import indicator_prices


class StrategiesMacd(CtpbeeApi):
    def __init__(self, contracts: List[str], with_tkinter: bool = False):
        super().__init__(self.__class__.__name__)
        # 接受合约
        if contracts is None:
            contracts = []
        self.with_tkinter = with_tkinter
        self.instrument_set = contracts
        # 完成界面
        if with_tkinter:
            # 创建界面
            self.tkinter_root = tk.Tk()
            self.tkinter_root.title('big_quant')
            # 为界面准备UI
            self.ui_dict = {}
            # 添加时间栏
            datetime_frame = '日期时间'
            self.ui_dict[datetime_frame] = tk.Label(self.tkinter_root, text='日期时间')
            self.ui_dict[datetime_frame].pack(side=tk.TOP, fill=tk.X)
            # 添加合约
            notebook = 'contract_notebook'
            self.ui_dict[notebook] = ttk.Notebook(self.tkinter_root)
            for contract in contracts:
                # ------------ 创建页面 ------------
                tab = 'contract_frame'
                self.ui_dict[tab] = tk.Frame(self.ui_dict[notebook])
                # 现价
                price_frame = 'contract_price_frame'
                self.ui_dict[f'{price_frame}.{contract}'] = tk.Label(self.ui_dict[tab], text='现价')
                self.ui_dict[f'{price_frame}.{contract}'].pack(side=tk.TOP, fill=tk.X)
                # 盘口
                price_frame = 'contract_position_frame'
                self.ui_dict[price_frame] = tk.Frame(self.ui_dict[tab])
                self.ui_dict[f'{price_frame}.{contract}.买1'] = tk.Label(self.ui_dict[price_frame], text='买1')
                self.ui_dict[f'{price_frame}.{contract}.买1'].pack(side=tk.LEFT)
                self.ui_dict[f'{price_frame}.{contract}.卖1'] = tk.Label(self.ui_dict[price_frame], text='卖1')
                self.ui_dict[f'{price_frame}.{contract}.卖1'].pack(side=tk.RIGHT)
                self.ui_dict[f'{price_frame}'].pack(side=tk.TOP, fill=tk.X)
                # 明细
                detail_frame = 'contract_detail_frame'
                self.ui_dict[detail_frame] = tk.Frame(self.ui_dict[tab])
                self.ui_dict[f'{detail_frame}.{contract}.多'] = tk.Text(self.ui_dict[detail_frame], width=17, height=10)
                self.ui_dict[f'{detail_frame}.{contract}.多'].pack(side=tk.LEFT, fill=tk.X)
                self.ui_dict[f'{detail_frame}.{contract}.空'] = tk.Text(self.ui_dict[detail_frame], width=17, height=10)
                self.ui_dict[f'{detail_frame}.{contract}.空'].pack(side=tk.RIGHT, fill=tk.X)
                self.ui_dict[f'{detail_frame}'].pack(side=tk.TOP, fill=tk.X)
                # 策略提示
                strategy_frame = 'contract_strategy_frame'
                self.ui_dict[f'{strategy_frame}.{contract}'] = tk.Text(self.ui_dict[tab], width=35, height=10)
                self.ui_dict[f'{strategy_frame}.{contract}'].pack(side=tk.BOTTOM, fill=tk.X)
                # ------------ 载入页面 ------------
                self.ui_dict[notebook].add(self.ui_dict[tab], text=contract)
            self.ui_dict[notebook].pack(side=tk.BOTTOM, fill=tk.X)

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
                logger.info(f'{key}-MACD计算-包含长度[{len(prices)}]')
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
        self.ui_dict['日期时间'].config(text=now_datetime)
        self.tkinter_root.update()
        return now_datetime

    def update_price(self, contract: str, price: str):
        text_key = f'contract_price_frame.{contract}'
        self.ui_dict[text_key].config(text=price)

    def update_position(self, contract: str, buy: str, sell: str):
        text_key = f'contract_position_frame.{contract}.买1'
        self.ui_dict[text_key].config(text=buy)
        text_key = f'contract_position_frame.{contract}.卖1'
        self.ui_dict[text_key].config(text=sell)
        self.tkinter_root.update()

    def update_detail(self, contract: str, detail: str):
        if detail is None:
            detail = ''
        if '↑' not in detail and '↓' not in detail:
            return
        detail_type = {'↑': '多', '↓': '空'}.get(detail.split('-')[1])
        text_key = f'contract_detail_frame.{contract}.{detail_type}'
        # TODO 绘制多空能量柱
        self.ui_dict[text_key].insert(tk.END, f'{detail}\n')
        self.ui_dict[text_key].see(tk.END)
        self.tkinter_root.update()

    def update_strategy(self, contract: str, strategy: str):
        if strategy is None:
            strategy = ''
        text_key = f'contract_strategy_frame.{contract}'
        self.ui_dict[text_key].insert(tk.END, strategy + '\n')
        self.ui_dict[text_key].see(tk.END)
        self.tkinter_root.update()

    def clear_text(self, clear_text_key: str):
        self.ui_dict[clear_text_key].delete('1.0', tk.END)
        self.tkinter_root.update()
