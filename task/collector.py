import os
from datetime import datetime
from typing import Callable, List

from loguru import logger

from comm import tool_classes, tool_scheduler
from load import data_loader


@tool_classes.ToolClasses.singleton
class Collector:
    @staticmethod
    def save_to_csv(func: Callable, code: str) -> None:
        logger.info(f'{code}-{func.__name__}...start...')
        # 提取数据
        df = func(code)
        # 数据保存路径
        base_path = '_data'
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        # 根据数据日期判断是否当日产生的数据
        now_date_str = datetime.now().strftime('%Y-%m-%d')
        data_date_str = df.loc[1]['日期']
        if data_date_str != now_date_str:
            logger.info(f'{code}-{func.__name__}...非当日数据，跳过...')
            return None
        # 保存文件
        target_path = os.path.join(base_path, f'{code}-{data_date_str}-{func.__name__}.csv')
        df.to_csv(target_path, index=False)
        logger.info(f'{code}-{func.__name__}...end...')
        return None

    @staticmethod
    def min_line_save_every_day(codes: List[str]) -> None:
        # 对所有代码添加收集任务
        for code in codes:
            tool_scheduler.ToolScheduler().scheduler.add_job(
                Collector().save_to_csv,
                'cron', hour='15', minute='00',
                args=[data_loader.SinaLoader().today_min_line, code],
                max_instances=8,
            )
        return None
