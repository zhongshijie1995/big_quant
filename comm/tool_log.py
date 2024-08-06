from loguru import logger


class ToolLog:
    @staticmethod
    def init_logger():
        log_path = '_log/last.log'
        logger.add(log_path, rotation="00:00", retention="10 days")
        logger.info('日志初始化完成！')
