from time import time, sleep
import random

from matplotlib import pyplot as plt

from pathholder import PathHolder
import imgcache


DELAY = 0.05

Timer = time()  # 定时器
NEXT = False    # 刷新图片显示
PAUSE = False   # 暂停
IMG = ''    # 当前图片数据


def show_image(args):
    global Timer, NEXT, IMG, PAUSE
    random.seed(float(args.seed))
    FLAG = float(args.time)  # 切换时间间隔

    # 配置随机路径生成器
    if args.targetpath == '目录.txt':
        Tree=False
        target=''
    else:
        Tree = True
        target = args.targetpath
    if args.mode == 'mongodb':
        from mongo import MongoBuilder
        mongodb = MongoBuilder(client=args.client, db=args.database, collection=args.collection, Tree=Tree, target=target)
        if args.initialize:
            mongodb.initialize()
        if args.update:
            mongodb.update()
        if args.clear:
            print('确认删除数据库表{}.{}吗？ [y/n]'.format(args.database, args.collection))
            if input() == 'y':
                mongodb.clear()
        if mongodb.datalength == 0:
            raise Exception('数据库表{}为空'.format(args.collection))
        pather = PathHolder(mongodb)
        print('数据库中有{}个图片路径'.format(pather.datalength))
    elif args.mode == 'ontime':
        from ontime import MethodOntime
        ontime = MethodOntime(Tree=Tree, target=target)
        pather = PathHolder(ontime)
        print('共找到{}个图片路径'.format(pather.datalength))

    imgcache.image_list_init(pather)
    lock = imgcache.list_filler(pather)     # 缓存线程
    lock.daemon = True  # 设为守护线程
    lock.start()    # 启动缓存线程

    if args.debug:
        print(pather.datalength)
    if not args.showimage:
        return -1

    # 按键动作
    def onkey(event):
        global IMG, Timer, NEXT, PAUSE
        if event.key == 'right':
            IMG = imgcache.next_image_func(pather, args.debug)
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

    # 滚轮动作
    def scroll(event):
        global IMG, Timer, NEXT
        if event.button == 'down':
            IMG = imgcache.next_image_func(pather, args.debug)
            Timer = time()
            NEXT = True
        if event.button == 'up':
            IMG = imgcache.previous_image(pather)
            Timer = time()
            NEXT = True

    # figoure axes 按键相关设置
    plt.rcParams['toolbar'] = 'None'
    plt.rcParams['keymap.quit'] = ['escape', 'q', 'ctrl+q']
    fig = plt.figure(num=42)
    fig.canvas.mpl_connect('key_press_event', onkey)
    fig.canvas.mpl_connect('scroll_event', scroll)
    fig.set_tight_layout('pad')
    fig.set_facecolor(args.background)
    ax = fig.add_subplot(111)

    manager = plt.get_current_fig_manager()
    if args.screensize == 'fullscreen':
        pass
        # manager.full_screen_toggle()
    else:
        size = args.screensize.split(',')
        manager.resize(float(size[0]), float(size[1]))

    # 可能会多出来个窗口
    if plt.fignum_exists(1):
        plt.close(1)

    IMG = IMG = imgcache.next_image_func(pather, args.debug)  # 第一个路径
    print('-' * 10 + '初始化完毕' + '-' * 10)

    while True:
        try:
            ax.clear()
            ax.axis('off')
            ax.imshow(IMG, interpolation='none', filternorm=False, resample=False)

            Timer = time()  # 定时器

            while True:
                if not plt.fignum_exists(42):   # 图片窗口被关闭
                    return 0
                if NEXT:  # 按下左右键、旋转
                    NEXT = False
                    break
                if time() - Timer >= FLAG:  # 到达指定时间间隔
                    if not PAUSE:   # 没有暂停
                        IMG = IMG = imgcache.next_image_func(pather, args.debug)
                        Timer = time()
                        break
                plt.pause(DELAY)
        except:
            raise

