import requests

url = 'http://hq.sinajs.cn/list=' + 'nf_' + 'RM2409'

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Referer': 'https://finance.sina.com.cn/',
}
response = requests.get(url, headers=header)
print(response.text)

import requests
import traceback
import re


def sina_future_request_intraday_1minute(ctrid):
    # 请求
    url = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20t1nf_" + \
          ctrid.upper() + "=/InnerFuturesNewService.getMinLine?symbol=" + ctrid.upper()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Referer': 'https://finance.sina.com.cn/'}
    stock_info = ""
    result = []
    try:
        page = requests.get(url, headers=headers)
        stock_info = page.text
        # print(stock_info)
    except Exception as e:
        errorWord = traceback.format_exc()
        print(errorWord)
    else:
        # 爬取到数据信息
        if stock_info != "":
            mt_info = stock_info.split("(")
            mt_info = mt_info[1]
            mt_info = re.sub("\)|;", "", mt_info)
            mt_info = eval(mt_info)
            result = mt_info
        else:
            result = []
    return result


result = sina_future_request_intraday_1minute('RM2409')
print(result)
