from ctpbee import CtpBee

from ctp import ctp_action, ctp_account, ctp_strategy, ctp_contract


def create_app() -> CtpBee:
    # 创建APP
    app = CtpBee('big_quant', __name__, action_class=ctp_action.CtpAction)
    # 添加账户
    app.config.from_mapping(ctp_account.CtpAccount().acct_dict.get('simnow-02'))
    # 添加策略
    app.add_extension(ctp_strategy.LogTick(ctp_contract.CtpContract().contracts))
    return app


if __name__ == '__main__':
    from ctpbee import hickey

    hickey.start_all(create_app)
