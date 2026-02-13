import argparse
from time import time
from msvcrt import getch
from sys import exit
import warnings
import traceback

from imageshow import show_image
from configtoargs import configtoargs

warnings.filterwarnings("ignore", ".*GUI is implemented.*")     # matplotlib2.0.2会跳出警告


def get_args_parser():
    parser = argparse.ArgumentParser(prog='Random Image Viewer ')
    parser.add_argument('-m', '--mode', choices=['ontime', 'mongodb'], default='ontime', help='选择路径生成模式 默认文件树缓存在内存中')
    parser.add_argument('-t', '--time', default=600, help='切换图片的时间间隔 单位是秒 默认600秒（10分钟）')
    parser.add_argument('--seed', default=time(), help='随机数生成器的种子')
    parser.add_argument('-b', '--background', default='k', help='设置背景颜色 默认为黑色')
    parser.add_argument("-v", "--version", action='version', version='%(prog)sv2.1', help='输出版本号')
    parser.add_argument('--screensize', default='fullscreen', help='指定窗口大小 默认为全屏 修改请用英文逗号分割宽高 宽在前 高在后')
    parser.add_argument('--client', default='mongodb://localhost:27017/', help='MongoDB地址 默认为本地')
    parser.add_argument('--database', default='RandomImage', help='MongoDB数据库名称 默认为RandomImage')
    parser.add_argument('--collection', default='ImagePath', help='MongoDB数据库表名称 默认为ImagePath')
    parser.add_argument('--targetpath', default='目录.txt', help='用于从指定目标文件中读取目录 默认为根目录下的 目录.txt')
    parser.add_argument('--initialize', action='store_true', help='初始化数据库')
    parser.add_argument('--update', action='store_true', help='更新数据库')
    parser.add_argument('--clear', action='store_true', help='删除数据库表   \033[31m谨慎操作\033[0m')
    parser.add_argument('--hideimage', action='store_true', help='是否显示图片 默认显示')
    parser.add_argument('--cache', action='store_true', help='是否使用缓存机制 默认使用')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--configfile', action='store_false', help='是否使用配置文件 默认使用')
    return parser


if __name__ == '__main__':
    print('程序初始化中...')

    parser = get_args_parser()
    args = parser.parse_args()

    if args.debug:
        args = parser.parse_args(['-d',
                                  '--mode=mongodb',
                                  # '--mode=ontime',
                                  '--collection=LIKES',
                                  '--time=600',
                                  '--configfile',
                                  '--screensize=1000,1000',
                                  # '--cache',
                                  # '--initialize',
                                  # '--update',
                                  # '--hideimage'`
                                  ])
    print('本次运行随机种子为:{}'.format(args.seed))

    if args.configfile:
        args = configtoargs()
        # print('使用配置文件')

    if args.debug:
        print('-'*10+'Debug模式已启用'+'-'*10)

    try:
        if args.initialize or args.update:
            if '+' in args.collection:
                raise ValueError('数据库表名中有非法字符“+”')
        status = show_image(args)   # 主程序
    except Exception as e:
        print('\n', traceback.format_exc())
        print('\n错误！', e.args[0])

    try:
        if status == 0:
            if args.debug:
                print('正常退出')
            else:   # 正常模式正常退出
                print('窗口关闭\n'+'-'*10+'按任意键退出程序'+'-'*10)
                getch()
                exit()
        elif status == -1:  # 不显示图片的模式
            print('不显示照片 程序结束')
            exit()
    except NameError:
        print('\n' + '-' * 10 + '按任意键退出程序' + '-' * 10)
        if args.debug:
            print('正常退出')
        else:
            getch()
            exit()
