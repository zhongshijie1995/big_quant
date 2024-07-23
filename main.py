from comm import data_loader

if __name__ == '__main__':
    s = data_loader.SinaLoader().get_realtime('000987')
    print(s)
    s = data_loader.SinaLoader().get_realtime('AU2409')
    print(s)
