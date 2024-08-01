# from load import data_loader
#
# if __name__ == '__main__':
#     # code = 'RM2409'
#     # s = data_loader.SinaLoader().get_today_min_line(code)
#     # buy_chance, sell_chance = strategy_simple.MACD().get_golden_death_cross(s)
#     # print('做多')
#     # print(buy_chance)
#     # print('做空')
#     # print(sell_chance)
#
#     codes = ['SA2409', 'RM2409', 'CS2409']
#     for code in codes:
#         data_loader.SinaLoader().save_line_to_csv(data_loader.SinaLoader().today_min_line, code)


import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def my_job(name):
    print(f"Executing job {name} at {time.strftime('%Y-%m-%d %H:%M:%S')}")


# 创建一个后台调度器
scheduler = BackgroundScheduler()

# 定时任务列表
tasks = [
    ('* * * * *', my_job, ('task1',)),  # 每小时的第0分钟执行task1
    ('*/2 * * * *', my_job, ('task2',))  # 每小时的第30分钟执行task2
]

# 遍历任务列表，添加任务到调度器
for cron_expression, func, args in tasks:
    scheduler.add_job(func, CronTrigger.from_crontab(cron_expression), args=args)

# 启动调度器
scheduler.start()

# 保持主线程运行，以便查看结果
try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # 关闭调度器
    scheduler.shutdown()
