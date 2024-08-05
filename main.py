from task import collector, holder, executor

if __name__ == '__main__':
    codes = [
        'SA2409',
        'RM2409',
        'CS2409',
    ]
    # 添加每日数据收集
    collector.Collector().min_line_save_every_day(codes)
    # 添加每分钟MACD策略
    executor.Executor().macd_chance_every_min(codes)
    # 保持定时任务
    holder.Holder().scheduler_keep()
