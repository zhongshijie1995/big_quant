import tkinter as tk
from multiprocessing import Process

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


def ctpbee_start():
    # 7*24自动上下线
    hickey.start_all(create_ctpbee_app)


def time_start():
    pass


def gui_start():
    root = tk.Tk()
    root.title('big_quant')

    time_entry = tk.Label(root, text='TimeTimeTimeTimeTimeTimeTimeTimeTimeTimeTimeTimeTimeTimeTimeTime')
    time_entry.pack()

    root.mainloop()


if __name__ == '__main__':
    # 开启时间程序
    # p_time = Process(target=time_start, args=())
    # p_time.start()
    # 开启ctpbee程序
    p_ctpbee = Process(target=ctpbee_start, args=())
    p_ctpbee.start()
    # GUI界面
    # gui_start()
