import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool

from loguru import logger

from comm import tool_classes, tool_sqlite


@tool_classes.ToolClasses.singleton
class DataSaver:
    def __init__(self, db_uri: str = '_data/main.db'):
        self.db_uri = db_uri
        # 准备数据库
        logger.info('初始化数据库')
        sql = """
        create table if not exists 期货_实时_秒级(
            代码 text,
            名称 text,
            开盘价 float,
            最高价 float,
            最低价 float,
            昨收价 float,
            买一价 float,
            卖一价 float,
            最新价 float,
            结算价 float,
            昨结算价 float,
            买量 int,
            卖量 int,
            持仓量 int,
            成交量 int,
            商品交易所简称 text,
            品种名简称 text,
            日期 text,
            时间 text
        );
        """
        tool_sqlite.ToolSqlite().exec(self.db_uri, sql)
        # 准备线程字典
        self.code_dict = {}
        self.thread_dict = {}

    def add_code(self, code: str):
        self.thread_dict[code] = [threading.Thread(target=self.add_code, args=(code,)), True]
        self.thread_dict[code].start()

    def del_code(self, code: str):
        pass

    def collect(self, code: str):
        logger.info(f'开始执行[{code}]-[{self.db_uri}]')
