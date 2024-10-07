# from ctpbee import CtpBee, CtpbeeApi
#
# from actions.action_base import ActionBase
# from strategies.strategy_macd import StrategiesMacd
#
#
# def create_ctpbee_app(act_config_path: str, strategy: CtpbeeApi) -> CtpBee:
#     # 创建APP
#     app = CtpBee('big_quant', __name__, action_class=ActionBase)
#     # 添加账户
#     app.config.from_json(act_config_path)
#     # 添加策略
#     app.add_extension(strategy)
#     # 返回APP
#     return app
#
#
# if __name__ == '__main__':
#     # 账户信息配置文件
#     act_config_path = './config/accounts/act_simnow_1.json'
#     # 自选信息配置文件
#     contract_path = './config/contracts/fav.txt'
#     with open(contract_path, 'r') as f:
#         contracts = [x.strip() for x in f.readlines() if not x.startswith('#')]
#     # 策略配置代码
#     strategy = StrategiesMacd(contracts, True)
#     # 启动服务
#     create_ctpbee_app(act_config_path, strategy).start()
#     # 显示界面
#     if strategy.with_tkinter:
#         strategy.tkinter_root.mainloop()
from comm.tool_record import ToolRecord

print(ToolRecord().read_from_date_file())
