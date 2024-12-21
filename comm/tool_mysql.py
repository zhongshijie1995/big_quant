import pandas as pd
import mysql.connector
from typing import List, Any, Callable

from loguru import logger

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class ToolMysql:

    def __init__(self):
        self.conn_dict = {}

    def get_conn(
            self,
            db_name: str,
            host: str = None,
            user: str = None,
            passwd: str = None,
            database: str = None
    ) -> mysql.connector.Connect:
        if db_name not in self.conn_dict:
            if None in [host, user, passwd, database]:
                logger.info(f'db_name[{db_name}]不存在且没有提供连接参数')
                return None
            logger.info(f'创建连接db_name[{db_name}]')
            self.conn_dict[db_name] = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database,
            )
        return self.conn_dict.get(db_name)

    def get_cursor(self, db_name: str, *args: Any, **kwargs: Any):
        conn = self.get_conn(db_name, *args, **kwargs)
        cur = conn.cursor()
        return conn, cur

    def exec(
            self,
            db_name: str,
            sql: str,
            host: str = None,
            user: str = None,
            passwd: str = None,
            database: str = None,
    ) -> None:
        conn, cursor = self.get_cursor(db_name, host, user, passwd, database)
        cursor.execute(sql)
        conn.commit()
        return None

    def query(
            self,
            db_name: str,
            sql: str,
            host: str = None,
            user: str = None,
            passwd: str = None,
            database: str = None,
    ) -> (List[str], List[Any]):
        conn, cursor = self.get_cursor(db_name, host, user, passwd, database)
        cursor.execute(sql)
        cols = [col[0] for col in cursor.description]
        return cols, cursor.fetchall()

    def export(
            self,
            db_name: str,
            sql: str,
            host: str = None,
            user: str = None,
            passwd: str = None,
            database: str = None,
            file_name_func: Callable = None,
    ):
        conn, cursor = self.get_cursor(db_name)
        cursor.execute(sql)
        cols = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        if len(data) == 0:
            return None
        pd.DataFrame(data, columns=cols).to_csv(file_name_func(data), index=False)
        return None
