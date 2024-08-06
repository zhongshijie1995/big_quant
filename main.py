from comm import tool_log, tool_scheduler
from task import collector, reporter

if __name__ == '__main__':
    tool_log.ToolLog.init_logger()
    codes = [
        'SA2409',
        'RM2409',
        'CS2409',
    ]
    # 添加每日数据收集
    collector.Collector().min_line_save_every_day(codes)
    # 添加每分钟MACD策略
    reporter.Reporter().macd_chance_every_min(codes)
    # 保持定时任务
    tool_scheduler.ToolScheduler().scheduler_keep()
