from comm import data_load

if __name__ == '__main__':
    s = data_load.SinaLoader().get_realtime_future('nf_AU2409')
    print(s)
