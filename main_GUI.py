from sys import exit
import warnings
import traceback

from imageshow import show_image
from configtoargs import configtoargs
from GUI import GUI, Message

warnings.filterwarnings("ignore", ".*GUI is implemented.*")     # matplotlib2.0.2会跳出警告

VERSION = 'v2.1'


if __name__ == '__main__':
    print('程序初始化中...')
    args = configtoargs()
    args.version = 'Random Image Viewer ' + VERSION
    print('本次运行随机种子为:{}'.format(args.seed))

    app = GUI(args)
    app.__enter__()
    args = app.args
    args.app = app

    if args.debug:
        print(args.__dict__)

    if app.end_state:
        if args.debug:
            print('-' * 10 + 'Debug模式已启用' + '-' * 10)

        try:
            if args.initialize or args.update:
                if '+' in args.collection:
                    raise ValueError('数据库表名中有非法字符“+”')
            show_image(args)  # 主程序
        except Exception as e:
            print('\n', traceback.format_exc())
            print('\n错误！', e.args[0])
            error = str(traceback.format_exc())+'\n\n错误！'+str(e.args[0])
            Message(error).__enter__()
    exit()

