# import efinance as ef
# import pandas as pd
# import tqdm
#
# df = ef.stock.get_realtime_quotes()
# cod_list = df['股票代码'].tolist()
# tmp = []
#
# for cod in tqdm.tqdm(cod_list):
#     tmp.append(ef.stock.get_quote_history(cod))
# result = pd.concat(tmp)
# result.to_csv('stock-history-20241225.csv', index=False)

import pandas as pd

data = pd.read_csv('_data/stock-history-20241225.csv')
print(data.groupby('股票代码').agg({'股票名称': ['first', 'count']}))