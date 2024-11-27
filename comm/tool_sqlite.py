import sqlite3
from typing import List, Any

import pandas as pd

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class ToolSqlite:

    def __init__(self):
        self.conn_dict = {}

    def get_conn(self, db_name: str) -> sqlite3.Connection:
        if db_name not in self.conn_dict:
            self.conn_dict[db_name] = sqlite3.connect(db_name, check_same_thread=False)
        return self.conn_dict.get(db_name)

    def get_cursor(self, db_name: str) -> (sqlite3.Connection, sqlite3.Cursor):
        conn = self.get_conn(db_name)
        cur = conn.cursor()
        return conn, cur

    def exec(self, db_name: str, sql: str) -> None:
        conn, cursor = self.get_cursor(db_name)
        cursor.execute(sql)
        conn.commit()
        return None

    def query(self, db_name: str, sql: str) -> (List[str], List[Any]):
        conn, cursor = self.get_cursor(db_name)
        cursor.execute(sql)
        cols = [col[0] for col in cursor.description]
        return cols, cursor.fetchall()

    def export(self, db_name: str, sql: str, filename: str) -> None:
        conn, cursor = self.get_cursor(db_name)
        cursor.execute(sql)
        cols = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        if len(data) == 0:
            return None
        pd.DataFrame(data, columns=cols).to_csv(filename, index=False)
        return None
