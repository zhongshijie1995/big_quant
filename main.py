from ctpbee import CtpBee, hickey

from ctp import ctp_accounts, ctp_actions, ctp_contracts, ctp_strategies


def create_ctpbee_app() -> CtpBee:
    # 创建APP
    app = CtpBee('big_quant', __name__, action_class=ctp_actions.CtpActions)
    # 添加账户
    app.config.from_mapping(ctp_accounts.CtpAccounts().acct_dict.get('simnow-01'))
    # 添加策略
    app.add_extension(ctp_strategies.MacdCross(ctp_contracts.CtpContracts().contracts))
    return app


if __name__ == '__main__':
    hickey.start_all(create_ctpbee_app)
