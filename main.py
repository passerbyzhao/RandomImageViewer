import argparse
import sys
from time import time
from msvcrt import getch
from sys import exit
import warnings
warnings.filterwarnings("ignore",".*GUI is implemented.*")

from imageshow import show_image


def get_args_parser():
    parser = argparse.ArgumentParser(prog='Random Image Viewer ')
    parser.add_argument('-m', '--mode', choices=['ontime', 'mongodb'], default='ontime', help='选择路径生成模式 默认文件树缓存在内存中')
    parser.add_argument('-t', '--time', default=600, help='切换图片的时间间隔 单位是秒 默认600秒（10分钟）')
    parser.add_argument('--seed', default=time(), help='随机数生成器的种子')
    parser.add_argument('-b', '--background', default='k', help='设置背景颜色 默认为黑色')
    parser.add_argument("-v", "--version", action='version', version='%(prog)sv0.1', help='输出版本号')
    parser.add_argument('--screensize', default='fullscreen', help='指定窗口大小 默认为全屏 修改请用英文逗号分割宽高 宽在前 高在后')
    parser.add_argument('--client', default='mongodb://localhost:27017/', help='MongoDB地址 默认为本地')
    parser.add_argument('--database', default='RandomImage', help='MongoDB数据库名称 默认为RandomImage')
    parser.add_argument('--collection', default='ImagePath', help='MongoDB数据库表名称 默认为ImagePath')
    parser.add_argument('--configfile', default='目录.txt', help='无实际意义')
    parser.add_argument('--initialize', action='store_true', help='初始化数据库')
    parser.add_argument('--update', action='store_true', help='更新数据库')
    parser.add_argument('--clear', action='store_true', help='删除数据库表   \033[31m谨慎操作\033[0m')
    parser.add_argument('--showimage', action='store_false', help='是否显示图片 默认显示')
    parser.add_argument('-d', '--debug', action='store_true')
    return parser


if __name__ == '__main__':
    parser = get_args_parser()

    args = parser.parse_args()
    if args.debug:
        args = parser.parse_args(['--mode=mongodb', '--collection=', '--time=600'])
    print('本次运行随机种子为:{}'.format(args.seed))
    if args.debug:
        print(type(args.time), args.time)
    print('程序初始化中...')
    status = show_image(args)
    if status == 0:
        print('窗口关闭\n'+'-'*10+'按任意键退出程序'+'-'*10)
        # if input('窗口关闭 按任意键退出程序'):
        #     exit()
        getch()
        exit()
    elif status == -1:
        print('不显示照片 程序结束')
        exit()
