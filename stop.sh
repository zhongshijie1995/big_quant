ps -ef | grep "big_quant.py" | awk '{print $2}' | xargs kill -9
