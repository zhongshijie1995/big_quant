from comm import data_load

if __name__ == '__main__':
    s = data_load.SinaLoader().get_realtime('000987')
    print(s)
    s = data_load.SinaLoader().get_realtime('AU2409')
    print(s)
