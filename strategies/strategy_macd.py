import tkinter as tk
import traceback
from datetime import datetime
from tkinter import ttk
from typing import List

from ctpbee import CtpbeeApi
from ctpbee.constant import ContractData, TickData
from loguru import logger

from ctp import ctp_tools, ctp_books


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
            # 为界面准备UI
            self.ui_dict = {}
            # 添加时间栏
            self.ui_dict['日期时间'] = tk.Label(self.tkinter_root, text='日期时间')
            self.ui_dict['日期时间'].pack(side=tk.TOP, fill=tk.X)
            # 添加合约
            self.ui_dict['contract_notebook'] = ttk.Notebook(self.tkinter_root)
            for contract in contracts:
                # ------------ 创建页面 ------------
                self.ui_dict['contract_frame'] = tk.Frame(self.ui_dict['contract_notebook'])
                # 现价
                self.ui_dict[f'contract.{contract}.现价'] = tk.Label(self.ui_dict['contract_frame'], text='现价')
                self.ui_dict[f'contract.{contract}.现价'].pack(side=tk.TOP, fill=tk.X)
                # 盘口
                self.ui_dict[f'contract_price_frame'] = tk.Frame(self.ui_dict['contract_frame'])
                self.ui_dict[f'contract_price.{contract}.买1'] = tk.Label(self.ui_dict[f'contract_price_frame'],
                                                                          text='买1')
                self.ui_dict[f'contract_price.{contract}.买1'].pack(side=tk.LEFT)
                self.ui_dict[f'contract_price.{contract}.卖1'] = tk.Label(self.ui_dict[f'contract_price_frame'],
                                                                          text='卖1')
                self.ui_dict[f'contract_price.{contract}.卖1'].pack(side=tk.RIGHT)
                self.ui_dict[f'contract_price_frame'].pack(side=tk.TOP, fill=tk.X)
                # 明细
                self.ui_dict[f'contract.{contract}.明细'] = tk.Text(self.ui_dict['contract_frame'])
                self.ui_dict[f'contract.{contract}.明细'].pack(side=tk.TOP, fill=tk.X)
                # 策略提示
                self.ui_dict[f'contract.{contract}.策略'] = tk.Text(self.ui_dict['contract_frame'])
                self.ui_dict[f'contract.{contract}.策略'].pack(side=tk.BOTTOM, fill=tk.X)
                # ------------ 载入页面 ------------
                self.ui_dict['contract_notebook'].add(self.ui_dict['contract_frame'], text=contract)
            self.ui_dict['contract_notebook'].pack(side=tk.BOTTOM, fill=tk.X)

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

    def on_realtime(self):
        self.update_time_bar()

    def update_time_bar(self):
        self.ui_dict['日期时间'].config(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.tkinter_root.update()

    def update_price_bar(self, contract: str, buy: str, sell: str):
        pass
