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
            elif key =='collection':
                configargs[key] = [k.strip() for k in config[n][key].split(',') if k.strip() != '']
            elif key in ['initialize', 'update', 'clear', 'hideimage', 'debug', 'cache', 'configfile']:
                configargs[key] = config[n].getboolean(key)
            else:
                configargs[key] = config[n][key]
    return config, configargs

def write_config(args):
    config = configparser.ConfigParser()
    config['Basic'] = {
        'mode': args.mode,
        'time': args.time,
        'background': args.background,
        'seed': '-1',
    }
    config['DataBase'] = {
        'client': args.client,
        'database': args.database,
        'collection': ','.join(args.collection),
        'initialize': args.initialize,
        'update': args.update,
        'clear': args.clear,
    }
    config['Advanced'] = {
        'configfile': args.configfile,
        'screensize': args.screensize,
        'hideimage': args.hideimage,
        'targetpath': args.targetpath,
        'cache': args.cache,
    }
    config['Other'] = {
        'debug': args.debug,
        'version': 'Random Image Viewer v2',
    }
    with open('config.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)


def check_configfile_option_and_save(args):
    config = configparser.ConfigParser()
    config.read('config.ini', encoding="utf-8-sig")
    if args.configfile:
        write_config(args)
    elif config['Advanced'].getboolean('configfile'):
        config['Advanced']['configfile'] = 'false'
        with open('config.ini', 'w', encoding='utf8') as configfile:
            config.write(configfile)



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
