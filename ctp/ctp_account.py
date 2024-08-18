from comm import tool_classes


@tool_classes.ToolClasses.singleton
class CtpAccount:
    acct_dict = {
        # simnow第一套环境-结算环境
        'simnow-01': {
            'CONNECT_INFO': {
                'userid': '229875',
                'password': 'Zsj@19951026',
                'brokerid': '9999',
                'md_address': 'tcp://180.168.146.187:10211',
                'td_address': 'tcp://180.168.146.187:10201',
                'product_info': '',
                'appid': 'simnow_client_test',
                'auth_code': '0000000000000000'
            },
            'INTERFACE': 'ctp',
            'MD_FUNC': True,
            'TD_FUNC': True,
        },
        # simnow第二套环境-7*24无结算环境
        'simnow-02': {
            'CONNECT_INFO': {
                'userid': '229875',
                'password': 'Zsj@19951026',
                'brokerid': '9999',
                'md_address': 'tcp://180.168.146.187:10130',
                'td_address': 'tcp://180.168.146.187:10131',
                'product_info': '',
                'appid': 'simnow_client_test',
                'auth_code': '0000000000000000'
            },
            'INTERFACE': 'ctp',
            'MD_FUNC': True,
            'TD_FUNC': True,
        }
    }
