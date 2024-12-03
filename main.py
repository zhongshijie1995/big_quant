import subprocess
import time

from future_ctp import contract_pick, ctp_record

open_time_list = [
    ('08:58', '15:02'),
    ('20:58', '23:59'),
    ('00:00', '02:32'),
]

ui_process = None
try:
    while True:
        now_hhmm = time.strftime("%H:%M")

        cmd = 'stop'
        for open_time in open_time_list:

            if open_time[0] <= now_hhmm <= open_time[1]:
                cmd = 'start'
        if cmd == 'start':
            try:
                if ui_process is not None:
                    continue
                print(f'----- start-[{now_hhmm}] 运行 -----')
                ui_process = subprocess.Popen(['python', 'big_quant.py'], stdout=subprocess.PIPE)
                print(f'----- start-[{now_hhmm}] 完毕 -----')
            except Exception as e:
                print(f'----- start-[{now_hhmm}]-异常[{e.__str__()}] -----')
        if cmd == 'stop':
            try:
                if ui_process is None:
                    continue
                if now_hhmm.startswith('15'):
                    contract_pick.pick_main_contract()
                    ctp_record.ToolRecord().export_and_clear_yesterday_from_sqlite()
                    time.sleep(300)
                print(f'----- stop-[{now_hhmm}] 运行 -----')
                ui_process.kill()
                print(f'----- stop-[{now_hhmm}] 完毕 -----')
            except Exception as e:
                print(f'----- start-[{now_hhmm}]-异常[{e.__str__()}] -----')
            finally:
                ui_process = None
        time.sleep(1)
except KeyboardInterrupt as e:
    print(f'中断定时主循环{e.__str__()}')
except Exception as e:
    print(f'中断定时主循环{e.__str__()}')
finally:
    if ui_process is not None:
        print(f'----- 强杀子进程 运行 -----')
        ui_process.kill()
        print(f'----- 强杀子进程 完毕 -----')
