import os.path
from datetime import datetime
from os import mkdir

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class ToolRecord:
    @staticmethod
    def append_to_date_file(txt: str, base_path: str = '_data') -> None:
        date_str = datetime.now().strftime('%Y%m%d')
        if not os.path.exists(base_path):
            os, mkdir(base_path)
        file_path = os.path.join(base_path, f'{date_str}.txt')
        with open(file_path, 'a') as f:
            f.write(txt + '\n')
        return None
