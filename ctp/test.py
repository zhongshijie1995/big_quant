from ctpbee import Action
from ctpbee import CtpBee, CtpbeeApi
from ctpbee.constant import *


class ActionMe(Action):
    def __init__(self, app):
        # 请记住要对父类进行实例化
        super().__init__(app)
        # # 通过add_risk_check接口添加风控
        # self.add_risk_check(self.sell)


class DoubleMA(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.instrument_set = ['AU2409.CFFEX']

    def on_contract(self, contract: ContractData):
        if contract.local_symbol in self.instrument_set:
            self.action.subscribe(contract.local_symbol)

    def on_tick(self, tick: TickData) -> None:
        """
        tick行情触发的时候会调用此函数，你可以通过print来打印它查看详情
        """
        print(tick)


def create_app():
    """
    工厂函数 创建app变量并加载相关变量，最后返回
    """
    app = CtpBee("ctpbee", __name__, action_class=ActionMe)  # 在此处我们创建我们的核心App。
    info = {
        "CONNECT_INFO": {
            "userid": "10000007",
            "password": "abc@123456",
            "brokerid": "1010",
            "md_address": "tcp://106.37.101.162:31205",
            "td_address": "tcp://106.37.101.162:31213",
            "product_info": "",
            "appid": "client_zhongshijie_1.0.0",
            "auth_code": "YHQHYHQHYHQHYHQH"
        },
        "INTERFACE": "ctp",  # 接口声明
        "TD_FUNC": True,  # 开启交易功能
    }
    app.config.from_mapping(info)
    double_ma = DoubleMA("double_ma")  # 创建我们的策略实例
    app.add_extension(double_ma)  # 将我们的策略通过app的add_extension接口加入进系统
    return app


if __name__ == "__main__":
    """
    通过ctpbee自己提供的24小时运行模块，让ctpbee能够自行运行程序，并在交易时间段和
    非交易时间段自动上下线
    """
    from ctpbee import hickey

    # 注意你在此处传入的是创建App的函数
    hickey.start_all(create_app)
