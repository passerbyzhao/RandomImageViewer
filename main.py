import argparse
from PIL import Image
from time import time
import random

from matplotlib import pyplot as plt

from pathholder import PathHolder


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
    parser.add_argument('--cache', default=15, help='随机图片列表中缓存路径的数量 默认为15')
    parser.add_argument('-d', '--debug', action='store_true')
    return parser


DELAY = 0.05

Timer = time()
NEXT = False
PAUSE = False
IMGPATH = ''
ANGLE = 0

def show_image(args):
    global Timer, NEXT, IMGPATH, PAUSE, CHANGE, ANGLE
    random.seed(args.seed)
    FLAG = float(args.time)    # 切换时间间隔

    # 配置随机路径生成器
    if args.mode == 'mongodb':
        from mongo import MongoBuilder
        mongodb = MongoBuilder(client=args.client, db=args.database, collection=args.collection)
        if args.initialize:
            mongodb.initialize()
        if args.update:
            mongodb.update()
        if args.clear:
            print('确认删除数据库表{}.{}吗？ [y/n]'.format(args.database, args.collection))
            if input()=='y':
                mongodb.clear()
        if mongodb.datalength == 0:
            raise Exception('数据库为空')
        pather = PathHolder(mongodb, args.cache)
    elif args.mode == 'ontime':
        from ontime import MethodOntime
        ontime = MethodOntime()
        pather = PathHolder(ontime, args.cache)

    if args.debug:
        print(pather.datalength)

    # 按键动作
    def onkey(event):
        global IMGPATH, Timer, NEXT, PAUSE, ANGLE
        if event.key == 'right':
            IMGPATH = pather.next_path()
            Timer = time()
            ANGLE = 0
            NEXT = True
        if event.key == 'left':
            IMGPATH = pather.previous_path()
            Timer = time()
            ANGLE = 0
            NEXT = True
        if event.key == '，' or event.key == ',':
            ANGLE -= 90
            NEXT = True
        if event.key == '。' or event.key == '.':
            ANGLE += 90
            NEXT = True
        if event.key == 'enter':
            PAUSE = not PAUSE

    # figoure axes 按键相关设置
    plt.rcParams['toolbar'] = 'None'
    plt.rcParams['keymap.quit'] = ['escape', 'q', 'ctrl+q']
    # plt.axis('off')   # USELESS
    fig = plt.figure(num=42)
    cid = fig.canvas.mpl_connect('key_press_event', onkey)
    fig.set_tight_layout('pad')
    fig.set_facecolor(args.background)
    ax = fig.subplots()

    manager = plt.get_current_fig_manager()

    if args.screensize == 'fullscreen':
        manager.full_screen_toggle()
    else:
        size = args.screensize.split(',')
        manager.resize(float(size[0]), float(size[1]))

    # 可能会多出来个窗口
    if plt.fignum_exists(1):
        plt.close(1)

    IMGPATH = pather.next_path()    # 第一个路径

    while True:
        img = Image.open(IMGPATH).rotate(ANGLE, expand=True)
        ax.clear()
        ax.axis('off')
        ax.imshow(img)
        # plt.draw()
        Timer = time()
        while True:
            if not plt.fignum_exists(42):
                raise Exception('主动关闭窗口 程序结束')
            if NEXT:    # 按下左或右键
                NEXT = False
                break
            if time()-Timer >= FLAG:    # 到达指定时间间隔
                if not PAUSE:
                    IMGPATH = pather.next_path()
                    Timer = time()
                    ANGLE = 0
                    break
            plt.pause(DELAY)


if __name__ == '__main__':
    parser = get_args_parser()
    args = parser.parse_args()
    print('seed:{}'.format(args.seed))
    if args.debug:
        print(type(args.time), args.time)
    show_image(args)
