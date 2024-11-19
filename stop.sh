ps -ef | grep big_quant | awk '{print $2}' | xargs kill -9
