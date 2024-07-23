from typing import Dict

import requests

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class SinaLoader:

    @staticmethod
    def code_transform(code: str) -> str:
        result = code
        # 期货
        if result[:2].isalpha():
            result = 'nf_' + result
        # 股票
        if result.isalnum():
            if result[:1] in ['6']:
                result = 'sh' + result
            if result[:1] in ['0', '3']:
                result = 'sz' + result
            if result[:1] in ['8']:
                result = 'bj' + result
        return result

    @staticmethod
    def realtime_struct(code: str, text: str) -> Dict:
        result = {}
        body = text[text.find('"'): text.rfind('"')].split(',')
        # 期货
        if code.startswith('nf_'):
            result['名称'] = body[0]
            result['开盘价'] = body[2]
            result['最高价'] = body[3]
            result['最低价'] = body[4]
            result['昨收价'] = body[5]
            result['买一价'] = body[6]
            result['卖一价'] = body[7]
            result['最新价'] = body[8]
            result['结算价'] = body[9]
            result['昨结算价'] = body[10]
            result['买量'] = body[11]
            result['卖量'] = body[12]
            result['持仓量'] = body[13]
            result['成交量'] = body[14]
            result['商品交易所简称'] = body[15]
            result['品种名简称'] = body[16]
            result['日期'] = body[17]
        # 股票
        if code[:2] in ['sh', 'sz', 'bj']:
            result['名称'] = body[0]
            result['开盘价'] = body[1]
            result['昨收价'] = body[2]
            result['最新价'] = body[3]
            result['最高价'] = body[4]
            result['最低价'] = body[5]
            result['成交量'] = body[8]
            result['成交额'] = body[9]
            result['买一量'] = body[10]
            result['买一价'] = body[11]
            result['买二量'] = body[12]
            result['买二价'] = body[13]
            result['买三量'] = body[14]
            result['买三价'] = body[15]
            result['买四量'] = body[16]
            result['买四价'] = body[17]
            result['买五量'] = body[18]
            result['买五价'] = body[19]
            result['卖一量'] = body[20]
            result['卖一价'] = body[21]
            result['卖二量'] = body[22]
            result['卖二价'] = body[23]
            result['卖三量'] = body[24]
            result['卖三价'] = body[25]
            result['卖四量'] = body[26]
            result['卖四价'] = body[27]
            result['卖五量'] = body[28]
            result['卖五价'] = body[29]
            result['日期'] = body[30]
            result['时间'] = body[31]

        # 处理数据类型
        for k in result.keys():
            if k[-1:] in ['价', '额']:
                result[k] = float(result[k])
            if k[-1:] in ['量']:
                result[k] = int(float(result[k]))
        return result

    @staticmethod
    def get_realtime(code: str) -> Dict:
        # 获取实时数据
        base_url = 'http://hq.sinajs.cn/list={}'
        header = {
            'user-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)',
            'Referer': 'https://finance.sina.com.cn/',
        }
        sina_code = SinaLoader().code_transform(code)
        response = requests.get(base_url.format(sina_code), headers=header)
        # 解析实时数据
        result = SinaLoader().realtime_struct(sina_code, response.text)
        # 返回结果
        return result
