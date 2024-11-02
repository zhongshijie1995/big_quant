import json
from typing import Dict

import pandas as pd
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
        body = text[text.find('"') + 1: text.rfind('"')].split(',')
        result['代码'] = code
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
            result['时间'] = f'{body[1][: 2]}:{body[1][2: 4]}:{body[1][4:]}'
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
    def realtime_quote(code: str) -> Dict:
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

    @staticmethod
    def today_min_line(code: str) -> pd.DataFrame:
        # 转换代码
        code = SinaLoader().code_transform(code)
        header = {
            'user-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)',
            'Referer': 'https://finance.sina.com.cn/',
        }
        # 发起请求
        if code.startswith('nf_'):
            url = f'https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20t1nf_{code}=/InnerFuturesNewService.getMinLine?symbol={code}'
        else:
            url = f'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={code}&scale=1&datalen=1023'
        response = requests.get(url, headers=header)
        data = response.text
        if code.startswith('nf_'):
            data = [x[:5] for x in eval(data[data.find('=(') + 2: data.rfind(');')])]
            cols = ['时间', '最新价', '均价', '成交量', '持仓量']
            result = pd.DataFrame(data, columns=cols)
            quote_result = SinaLoader().realtime_quote(code)
            result['日期'] = quote_result['日期']
            result['代码'] = quote_result['代码']
            result['名称'] = quote_result['名称']
            result = result.astype({
                '最新价': float,
                '均价': float,
                '成交量': int,
                '持仓量': int,
            })
        else:
            data = json.loads(data)
            result = pd.DataFrame(data)
            en_cols = ['amount', 'close', 'day', 'high', 'low', 'ma_price10', 'ma_price30', 'ma_price5', 'ma_volume10', 'ma_volume30', 'ma_volume5', 'open', 'volume']
            cols = ['成交额', '收盘价', '日期时间', '最高价', '最低价', '均线10', '均线30', '均线5', '均量10', '均量30', '均量5', '开盘价', '成交量']
            result = result[en_cols]
            result.columns = cols
        return result
