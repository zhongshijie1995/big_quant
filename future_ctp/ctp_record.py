import os.path
from datetime import datetime, timedelta
from os import mkdir
from typing import List, Dict, Any

from loguru import logger

from comm import tool_classes
from comm.tool_sqlite import ToolSqlite


@tool_classes.ToolClasses.singleton
class ToolRecord:
    @staticmethod
    def append_to_date_file(txt: str, base_path: str = '_data') -> None:
        now = datetime.now()
        if datetime.now().strftime('%H:%M:%S') > '21:00:00':
            now = now + timedelta(days=1)
        date_str = now.strftime('%Y%m%d')
        if not os.path.exists(base_path):
            os, mkdir(base_path)
        file_path = os.path.join(base_path, f'{date_str}.txt')
        with open(file_path, 'a') as f:
            f.write(txt + '\n')
        return None

    @staticmethod
    def read_from_date_file(base_path: str = '_data', date_str: str = None) -> List[Dict[str, Any]]:
        result = []
        try:
            if date_str is None:
                date_str = datetime.now().strftime('%Y%m%d')
            with open(os.path.join(base_path, f'{date_str}.txt'), 'r') as f:
                for line in f.readlines():
                    result.append(eval(line.strip()))
        except:
            logger.info(f'未找到历史数据{date_str}')
        return result

    @staticmethod
    def init_sqlite():
        db_name = '_data/main.db'
        sql = """
        create table if not exists TickData(
            时间 text,
            代码 text,
            交易所 text,
            品种名 text,
            成交量 integer,
            最新价 integer,
            最新量 float,
            涨停 float,
            跌停 float,
            持仓量 integer,
            均价 float,
            结算价 float,
            昨结算价 float,
            昨持仓量 integer,
            开盘价 float,
            最高价 float,
            最低价 float,
            昨收盘价 float,
            成交金额 float,
            买价1 float,
            买价2 float,
            买价3 float,
            买价4 float,
            买价5 float,
            卖价1 float,
            卖价2 float,
            卖价3 float,
            卖价4 float,
            卖价5 float,
            买量1 integer,
            买量2 integer,
            买量3 integer,
            买量4 integer,
            买量5 integer,
            卖量1 integer,
            卖量2 integer,
            卖量3 integer,
            卖量4 integer,
            卖量5 integer,
            明细 text
        );
        """
        ToolSqlite().exec(db_name, sql)

    @staticmethod
    def append_to_sqlite(d: Dict[str, Any]):
        db_name = '_data/main.db'
        cols = []
        datas = []
        for k, v in d.items():
            cols.append(k)
            datas.append(f'\'{v}\'')
        sql = f"""
        insert into TickData ({','.join(cols)}) values ({','.join(datas)});
        """
        ToolSqlite().exec(db_name, sql)

    @staticmethod
    def read_from_sqlite(date_str: str = None) -> List[Dict[str, Any]]:
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        db_name = '_data/main.db'
        sql = f"""
        select * from TickData where substring(时间, 1, 10) == '{date_str}';
        """
        result = []
        cols, rows = ToolSqlite().query(db_name, sql)
        for row in rows:
            tmp_row = dict(zip(cols, row))
            result.append(tmp_row)
        return result

