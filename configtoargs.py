import configparser
from time import time


# 读取配置文件并返回字典
def read_config():
    configargs = {}
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini', encoding="utf-8-sig")
    for n in config.sections():
        for key in config[n]:
            if key == 'seed':
                if config[n][key] == '-1':
                    configargs[key] = time()
                else:
                    configargs[key] = config[n][key]
            elif key in ['initialize', 'update', 'clear', 'showimage', 'debug']:
                configargs[key] = config[n].getboolean(key)
            else:
                configargs[key] = config[n][key]
    return config, configargs


# 用于模仿args的类
class Args:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# 返回模仿的args
def configtoargs():
    _, args = read_config()
    args = Args(**args)
    return args


if __name__ == '__main__':
    config, args = read_config()
    a = Args(**args)
    print(a.__dict__)

    print('Done')
