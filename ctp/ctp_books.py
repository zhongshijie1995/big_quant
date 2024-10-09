from typing import List, Dict, Any

from comm import tool_classes, tool_record
from comm.tool_record import ToolRecord
from ctp import ctp_tools


@tool_classes.ToolClasses.singleton
class CtpBooks:

    def __init__(self, max_len: int = 2 * 60 * 60 * 12):
        self.max_len: int = max_len
        self.books: Dict[str, List[Dict[str, Any]]] = {}

    def append(self, k: str, v: Dict[str, Any], real_time: bool = True):
        # 若账本不存在此合约，则新建账本
        if k not in self.books:
            # 新建账本
            self.books[k] = []
            # 拼接今日之数据
            today_tick_list = ToolRecord().read_from_date_file()
            for tick in today_tick_list:
                self.append(k, tick, real_time=False)
        # 若账本中已含有1条以上记录，则计算明细
        if len(self.books[k]) >= 1:
            l = self.query(k, -1, None)[0]
            v['明细'] = ctp_tools.CtpTools().parse_detail(l, v)['汇总']
        # 插入账本
        self.books[k].append(v)
        # 控制账本长度
        if len(self.books[k]) > self.max_len:
            self.books[k].pop(0)
        # 保存账本历史
        if real_time:
            tool_record.ToolRecord().append_to_date_file(str(v))

    def query(self, k: str, start: int = None, end: int = None) -> List[Dict[str, Any]]:
        data = self.books.get(k)
        if data is None:
            return []
        return data[start:end]

    def keys(self) -> List[str]:
        return list(self.books.keys())

    def reset(self):
        self.books.clear()
