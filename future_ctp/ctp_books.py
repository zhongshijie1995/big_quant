from typing import List, Dict, Any

from loguru import logger

from comm import tool_classes, tool_record
from comm.tool_record import ToolRecord
from future_ctp import ctp_tools


@tool_classes.ToolClasses.singleton
class CtpBooks:

    def __init__(self, max_len: int = 2 * 60 * 60 * 24):
        self.max_len: int = max_len
        self.books: Dict[str, List[Dict[str, Any]]] = {}
        self.detail: Dict[str, Dict[str, int]] = {}

    def append(self, k: str, v: Dict[str, Any], real_time: bool = True):
        # 若账本不存在此合约，则新建账本
        if k not in self.books:
            # 新建账本
            self.books[k] = []
            self.detail[k] = {k: 0 for k in ['空开', '多平', '双开', '双平', '多换', '空换', '空平', '多开']}
            # 拼接今日之数据
            today_tick_list = ToolRecord().read_from_sqlite()
            logger.info('---- 拼接今日之数据 start ----')
            for tick in today_tick_list:
                if tick['代码'] == k:
                    self.append(k, tick, real_time=False)
            logger.info(f'[{k}]-拼接[{len(self.books[k])}]条数据')
            logger.info('---- 拼接今日之数据 end----')
        # 若账本中已含有1条以上记录，则计算明细
        if len(self.books[k]) >= 1:
            l = self.query(k, -1, None)[0]
            v['明细'] = ctp_tools.CtpTools().parse_detail(l, v)['汇总']
            detail_type = v['明细'].split('-')[0]
            if detail_type != '未知':
                detail_num = int(v['明细'].split('-')[2])
                self.detail[k][detail_type] += detail_num
        # 插入账本
        self.books[k].append(v)
        # 控制账本长度
        if len(self.books[k]) > self.max_len:
            self.books[k].pop(0)
        # 保存账本历史
        if real_time:
            tool_record.ToolRecord().append_to_sqlite(v)

    def query(self, k: str, start: int = None, end: int = None) -> List[Dict[str, Any]]:
        data = self.books.get(k)
        if data is None:
            return []
        return data[start:end]

    def get_detail(self, k: str) -> Dict[str, int]:
        return self.detail.get(k)

    def keys(self) -> List[str]:
        return list(self.books.keys())

    def reset(self):
        self.books.clear()
        self.detail.clear()
