import os.path
import traceback
from datetime import datetime, timedelta
from os import mkdir
from typing import List, Dict, Any

from loguru import logger

from comm import tool_classes


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
