from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import ContractData, TickData


class DemoStrat(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.instrument_set = ['SA501.CZCE']

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
    app.config.from_json('simnow-02.json')
    app.add_extension(DemoStrat('test'))
    app.start()
