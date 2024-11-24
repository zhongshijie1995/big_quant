# from synthesis_restapi import data_loader
#
# for i in range(10):
#     s = data_loader.SinaLoader().realtime_quote('SA2501')
#     print(s)
from synthesis_restapi import data_saver

data_saver.DataSaver().add_code('SA0')