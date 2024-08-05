import datetime
from typing import List

from loguru import logger

from comm import tool_classes, tool_scheduler, tool_datetime
from load import data_loader
from strategy import strategy_simple


@tool_classes.ToolClasses.singleton
class Executor:
    @staticmethod
    def report_macd_chance(code: str):
        data = data_loader.SinaLoader().today_min_line(code)
        chance = strategy_simple.MACD().golden_death_cross(data)
        now_time_str = datetime.datetime.now().strftime('%H:%M')
        result = chance[
            chance['时间'].apply(lambda x: tool_datetime.ToolDatetime().calc_between_minutes(x, now_time_str) <= 1)]
        if result.shape[0] > 0:
            report_data = result.iloc[-1].to_dict()
            report_time = report_data["时间"]
            report_name = report_data["名称"]
            report_price = report_data["最新价"]
            report_type = ','.join([k for k, v in report_data.items() if v is True])
            logger.info(f'{report_time} - {report_name} - {report_price} - {report_type}')

    @staticmethod
    def macd_chance_every_min(codes: List[str]):
        # 对所有代码添加收集任务
        hour_str_list = ['21-23', '9-15']
        for code in codes:
            for hour_str in hour_str_list:
                tool_scheduler.ToolScheduler().scheduler.add_job(
                    Executor().report_macd_chance,
                    'cron', hour=hour_str, minute='*',
                    args=[code]
                )
        return None
