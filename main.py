import datetime

import chinese_calendar
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


def need_run() -> bool:
    # 获取当前时间
    now = datetime.datetime.now()
    # 1.交易时间必须是工作日
    if chinese_calendar.is_workday(now):
        # 1.1 今日工作日，有日盘
        if now.hour <= 15:
            return True
        # 1.2 今日工作日，有2种情况有夜盘
        if now.hour > 15:
            # 1.2.1 明天也是工作日
            if chinese_calendar.is_workday(now + datetime.timedelta(days=1)):
                return True
            # 1.2.2 明天不是特殊节假日
            tomorrow_detail = chinese_calendar.get_holiday_detail(now + datetime.timedelta(days=1))
            if tomorrow_detail[0] and tomorrow_detail[1] is None:
                return True
    return False


if __name__ == '__main__':
    if not need_run():
        exit()
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
