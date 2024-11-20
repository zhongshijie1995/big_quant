import subprocess
import time

open_time_list = [
    ('08:55', '15:05'),
    ('20:55', '02:05')
]

ui_process = None
while True:
    now_hhmm = time.strftime("%H:%M")

    cmd = 'stop'
    for open_time in open_time_list:
        if open_time[0] < now_hhmm < open_time[1]:
            cmd = 'start'
    if cmd == 'start':
        try:
            if ui_process is not None:
                continue
            print(f'----- start-[{now_hhmm}] 运行 -----')
            ui_process = subprocess.Popen(['python', 'big_quant.py'], stdout=subprocess.PIPE)
            print(f'----- start-[{now_hhmm}] 完毕 -----')
        except Exception as e:
            print(f'----- start-[{now_hhmm}]-异常[{e.message}] -----')
    if cmd == 'stop':
        try:
            if ui_process is None:
                continue
            print(f'----- stop-[{now_hhmm}] 运行 -----')
            ui_process.kill()
            print(f'----- stop-[{now_hhmm}] 完毕 -----')
        except Exception as e:
            print(f'----- start-[{now_hhmm}]-异常[{e.message}] -----')
        finally:
            ui_process = None
    time.sleep(1)
