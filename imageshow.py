from time import time, sleep
import random

from matplotlib import pyplot as plt

from pathholder import PathHolder
import imgcache


DELAY = 0.05

Timer = time()
NEXT = False
PAUSE = False
IMG = ''


def show_image(args):
    global Timer, NEXT, IMG, PAUSE, CHANGE
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
        pather = PathHolder(mongodb)
        print('数据库中有{}个图片路径'.format(pather.datalength))
    elif args.mode == 'ontime':
        from ontime import MethodOntime
        ontime = MethodOntime()
        pather = PathHolder(ontime)
        print('共找到{}个图片路径'.format(pather.datalength))

    imgcache.image_list_init(pather)
    lock = imgcache.list_filler(pather)
    lock.daemon = True
    lock.start()

    if args.debug:
        print(pather.datalength)

    if not args.showimage:
        return -1
    # print('正在准备图片')
    # 按键动作
    def onkey(event):
        global IMG, Timer, NEXT, PAUSE
        if event.key == 'right':
            IMG = imgcache.next_image(pather).run()
            Timer = time()
            NEXT = True
        if event.key == 'left':
            IMG = imgcache.previous_image(pather)
            Timer = time()
            NEXT = True
        if event.key == '，' or event.key == ',':
            IMG = IMG.rotate(-90, expand=True)
            NEXT = True
        if event.key == '。' or event.key == '.':
            IMG = IMG.rotate(90, expand=True)
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
    ax = fig.add_subplot(111)
    # print(type(ax))

    manager = plt.get_current_fig_manager()

    if args.screensize == 'fullscreen':
        manager.full_screen_toggle()
    else:
        size = args.screensize.split(',')
        manager.resize(float(size[0]), float(size[1]))

    # 可能会多出来个窗口
    if plt.fignum_exists(1):
        plt.close(1)

    IMG = imgcache.next_image(pather).run()    # 第一个路径
    print('-'*10+'初始化完毕'+'-'*10)
    while True:
        # if args.debug:
        #     print(IMG)
        # flagtime = time()
        # print('图片读取时间：{}'.format(time()-flagtime))
        # flagtime = time()
        # if ANGLE % 360 != 0:
        #     IMG = IMG.rotate(ANGLE, expand=True)
        # print('图片旋转时间：{}'.format(time() - flagtime))
        # flagtime = time()
        ax.clear()
        ax.axis('off')
        ax.imshow(IMG, interpolation='none', filternorm=False, resample=False)
        # print('图片显示时间：{}'.format(time() - flagtime))
        # flagtime = time()

        # plt.pause(DELAY)
        Timer = time()

        while True:
            if not plt.fignum_exists(42):
                return 0
            if NEXT:    # 按下左或右键
                NEXT = False
                break
            if time()-Timer >= FLAG:    # 到达指定时间间隔
                if not PAUSE:
                    IMG = imgcache.next_image(pather).run()
                    Timer = time()
                    break
            # sleep(DELAY)
            plt.pause(DELAY)

