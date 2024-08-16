from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import ContractData, TickData


class DemoStrat(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.instrument_set = ['sa2501.SHFE']

    def on_contract(self, contract: ContractData):
        if contract.local_symbol in self.instrument_set:
            self.action.subscribe(contract.local_symbol)

    def on_tick(self, tick: TickData) -> None:
        """
        tick行情触发的时候会调用此函数，你可以通过print来打印它查看详情
        """
        print(tick)


if __name__ == '__main__':
    app = CtpBee('demo', __name__)
    # info = {
    #     "CONNECT_INFO": {
    #         "userid": "10000007",
    #         "password": "abc@123456",
    #         "brokerid": "1010",
    #         "md_address": "tcp://106.37.101.162:31205",
    #         "td_address": "tcp://106.37.101.162:31213",
    #         "product_info": "",
    #         "appid": "client_zhongshijie_1.0.0",
    #         "auth_code": "YHQHYHQHYHQHYHQH"
    #     },
    #     "INTERFACE": "ctp",  # 接口声明
    #     "TD_FUNC": True,  # 开启交易功能
    # }
    info = {
        "CONNECT_INFO": {
            "userid": "229875",
            "password": "Zsj@19951026",
            "brokerid": "9999",
            "md_address": "tcp://180.168.146.187:10201",  # simnow 第一套
            "td_address": "tcp://180.168.146.187:10211",  # simnow 第一套
            "product_info": "",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000"
        },
        "INTERFACE": "ctp",  # 接口声明
        "TD_FUNC": True,  # 开启交易功能
    }
    app.config.from_mapping(info)
    app.add_extension(DemoStrat('test'))
    app.start()
