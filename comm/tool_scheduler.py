import time
import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class ToolScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def get_scheduler(self):
        return self.scheduler

    @staticmethod
    def scheduler_keep():
        logger.info("定时任务保持中...start...")
        try:
            while True:
                time.sleep(60)
        except Exception as e:
            logger.info('定时任务主线程异常退出[{}]-[{}]', e, traceback.format_exc())
        finally:
            logger.info('定时任务资源释放...start...')
            ToolScheduler().scheduler.shutdown()
            logger.info('定时任务资源释放...end...')
            logger.info("定时任务保持中...end...")
