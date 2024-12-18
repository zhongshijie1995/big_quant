from comm import tool_mysql
import pandas as pd

s = pd.read_csv('_data/2024-12-17.csv')

# result = tool_mysql.ToolMysql().query(
#     'big_quant',
#     'select * from TickData',
#     host='localhost',
#     user='big_quant',
#     passwd='big_quant',
#     database='big_quant'
# )
# print(result)