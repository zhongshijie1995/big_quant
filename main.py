from ctpbee import CtpBee, CtpbeeApi

from future_ctp.action_base import ActionBase
from future_ctp.strategy_macd import StrategiesMacd


def create_ctpbee_app(act_config_path: str, strategy: CtpbeeApi) -> CtpBee:
    # 创建APP
    app = CtpBee('big_quant', __name__, action_class=ActionBase)
    # 添加账户
    app.config.from_json(act_config_path)
    # 添加策略
    app.add_extension(strategy)
    # 返回APP
    return app


if __name__ == '__main__':
    # 账户信息配置文件
    act_config_path = 'future_ctp/act_simnow_1.json'
    # 自选信息配置文件
    contract_path = 'future_ctp/contracts_fav.txt'
    with open(contract_path, 'r') as f:
        contracts = [x.strip() for x in f.readlines() if not x.startswith('#')]
    # 策略配置代码
    strategy = StrategiesMacd(contracts, True)
    # 启动服务
    app = create_ctpbee_app(act_config_path, strategy)
    app.start()
    # 显示界面
    if strategy.with_tkinter:
        strategy.tkinter_root.mainloop()
