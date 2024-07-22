import requests

from comm import tool_classes


@tool_classes.ToolClasses.singleton
class SinaLoader:
    realtime_base_url = 'http://hq.sinajs.cn/list={}'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Referer': 'https://finance.sina.com.cn/',
    }

    def get_realtime_future(self, code: str):
        response = requests.get(self.realtime_base_url.format(code), headers=self.header)
        if response.status_code != 200:
            print('200 OK')
        return response.text
