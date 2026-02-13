from time import time, sleep
import random

from matplotlib import pyplot as plt
from PIL import Image

from pathholder import PathHolder


DELAY = 0.05

Timer = time()  # 定时器
NEXT = False    # 刷新图片显示
PAUSE = False   # 暂停
IMG = ''    # 当前图片数据
IMGPATH = ''    # 当前图片路径
LIKECOLLECTION = ''
WALLPAPERCOLLECTION = ''

def show_image(args):
    # 图片缓冲相关 暂时停用
    # if args.cache:
    #     import imgcache
    # else:
    #     from imgwithoutcache import ImgCache
    #     imgcache = ImgCache()
    from imgwithoutcache import ImgCache
    imgcache = ImgCache()
    global Timer, NEXT, IMG, PAUSE, IMGPATH, LIKECOLLECTION, WALLPAPERCOLLECTION
    random.seed(float(args.seed))

    # 配置随机路径生成器
    if args.targetpath == '目录.txt':
        Tree=False
        target=''
    else:
        Tree = True
        target = args.targetpath
    if args.mode == 'mongodb':
        from mongo import MongoBuilder

        from pymongo import MongoClient
        client = MongoClient(args.client)
        db = client[args.database]
        LIKECOLLECTION = db['LIKES']
        WALLPAPERCOLLECTION = db['WALLPAPERS']

        mongodb_list = args.collection
        mongodb = MongoBuilder(client=args.client, db=args.database, collection=args.collection, Tree=Tree, target=target)

        if mongodb.datalength == 0:
            raise Exception('数据库表{}为空'.format(args.collection))
        if args.initialize:
            if len(mongodb_list) != 1:
                raise Exception('选中多个数据库,无法初始化')
            mongodb.initialize()
        if args.update:
            if len(mongodb_list) != 1:
                raise Exception('选中多个数据库,无法更新')
            mongodb.update()
        if args.clear:
            if len(mongodb_list) != 1:
                raise Exception('选中多个数据库,无法删除')
            print('确认删除数据库表{}.{}吗？ [y/n]'.format(args.database, args.collection))
            if input() == 'y':
                mongodb.clear()

        pather = PathHolder(mongodb)
        print('数据库中有{}个图片路径'.format(pather.datalength))
    elif args.mode == 'ontime':
        from ontime import MethodOntime
        ontime = MethodOntime(Tree=Tree, target=target)
        pather = PathHolder(ontime)
        print('共找到{}个图片路径'.format(pather.datalength))

    # 图片缓存相关 暂时停用
    # if args.cache:
    #     imgcache.image_list_init(pather)
    #     lock = imgcache.list_filler(pather)     # 缓存线程
    #     lock.daemon = True  # 设为守护线程
    #     lock.start()    # 启动缓存线程

    if args.debug:
        print(pather.datalength)
    if args.hideimage:
        return -1

    # 按键动作
    def onkey(event):
        global IMG, Timer, NEXT, PAUSE, IMGPATH, LIKECOLLECTION, WALLPAPERCOLLECTION
        if event.key == 'right':
            IMG, IMGPATH = imgcache.next_image_func(pather, args.debug)
            Timer = time()
            NEXT = True
        if event.key == 'left':
            IMG, IMGPATH = imgcache.previous_image(pather)
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
        if event.key == 'ctrl+s':
            with open('SavedSeed.txt', "w", encoding="utf-8") as f:
                f.write(str(args.seed))
            NEXT = True
        if event.key == 'l':    # 添加喜爱列表
            if args.mode == 'mongodb':
                # LIKECOLLECTION.update_one({'path':IMGPATH}, {'$setOnInsert':{'path':IMGPATH}}, upsert=True)
                print(f'Liked: {IMGPATH}')
            # print('l is pressed')
            NEXT = True
        if event.key == 'ctrl+l':  # 删除喜爱列表
            if args.mode == 'mongodb':
                LIKECOLLECTION.find_one_and_delete({'path':IMGPATH})
                print(f'Unliked: {IMGPATH}')
            # print('control+l is pressed')
            NEXT = True
        if event.key == 'w':    # 添加壁纸列表
            if args.mode == 'mongodb':
                WALLPAPERCOLLECTION.update_one({'path':IMGPATH}, {'$setOnInsert':{'path':IMGPATH}}, upsert=True)
                print(f'Wallpaper added: {IMGPATH}')
            # print('l is pressed')
            NEXT = True
        if event.key == 'ctrl+w':  # 删除壁纸列表
            if args.mode == 'mongodb':
                WALLPAPERCOLLECTION.find_one_and_delete({'path':IMGPATH})
                print(f'Wallpaper removed: {IMGPATH}')
            # print('control+l is pressed')
            NEXT = True
        # if event.key == 'ctrl+right':   # 目录中的下一个文件
        #     if args.mode == 'mongodb':
        #         pass
        #         # img = Image.open(path)
        #     NEXT = True
        # if event.key == 'ctrl+left':    # 目录中的上一个文件
        #     if args.mode == 'mongodb':
        #         pass
        #     NEXT = True

    # 鼠标按键动作
    def onbutton(event):
        global NEXT, IMGPATH, LIKECOLLECTION, WALLPAPERCOLLECTION
        # print(event.key)
        if event.button == 9:  # 添加喜爱列表 鼠标前进键
            if args.mode == 'mongodb':
                LIKECOLLECTION.update_one({'path': IMGPATH}, {'$setOnInsert': {'path': IMGPATH}}, upsert=True)
                print(f'Liked: {IMGPATH}')
            # print('9 is pressed')
            NEXT = True
        if event.button == 8:  # 添加喜爱列表 鼠标后退键
            if args.mode == 'mongodb':
                WALLPAPERCOLLECTION.update_one({'path': IMGPATH}, {'$setOnInsert': {'path': IMGPATH}}, upsert=True)
                print(f'Wallpaper added: {IMGPATH}')
            # print('8 is pressed')
            NEXT = True

    # 滚轮动作
    def scroll(event):
        global IMG, Timer, NEXT, IMGPATH
        if event.button == 'down':
            IMG, IMGPATH = imgcache.next_image_func(pather, args.debug)
            # print(f'Scrolling: {IMGPATH}')
            Timer = time()
            NEXT = True
        if event.button == 'up':
            IMG, IMGPATH = imgcache.previous_image(pather)
            # print(f'Scrolling back: {IMGPATH}')
            Timer = time()
            NEXT = True

    # figoure axes 按键相关设置
    plt.rcParams['toolbar'] = 'None'
    plt.rcParams['keymap.quit'] = ['escape', 'q', 'ctrl+q']
    fig = plt.figure(num=42)
    fig.canvas.mpl_connect('key_press_event', onkey)
    fig.canvas.mpl_connect('button_press_event', onbutton)
    fig.canvas.mpl_connect('scroll_event', scroll)
    fig.set_tight_layout('pad')
    fig.set_facecolor(args.background)
    ax = fig.add_subplot(111)

    manager = plt.get_current_fig_manager()
    # manager.window.wm_geometry('+10+10')
    if args.screensize == 'fullscreen':
        pass
        # manager.full_screen_toggle()
    else:
        size = args.screensize.split(',')
        manager.resize(float(size[0]), float(size[1]))

    # 可能会多出来个窗口
    if plt.fignum_exists(1):
        plt.close(1)

    IMG, IMGPATH = imgcache.next_image_func(pather, args.debug)  # 第一个路径
    print('-' * 10 + '初始化完毕' + '-' * 10)

    try:
        args.app.Window.destroy()
    except:
        pass
    try:
        image_display(ax, pather, args, fig, imgcache)
    except:
        raise
    finally:    # 为多线程预留 停止线程
        pass

# from matplotlib import backend_bases
def image_display(ax, pather, args, fig, imgcache):
    global Timer, NEXT, IMG, PAUSE, IMGPATH
    FLAG = float(args.time)  # 切换时间间隔
    plt.pause(0.0001)   # 显示窗口
    while True:
        try:
            ax.clear()
            ax.axis('off')
            ax.imshow(IMG, interpolation='none', filternorm=False, resample=False)
            Timer = time()  # 定时器
            fig.canvas.draw_idle()  # 刷新窗口
            while True:
                if not plt.fignum_exists(42):   # 图片窗口被关闭
                    return 0
                if NEXT:  # 按下左右键、旋转
                    NEXT = False
                    break
                if FLAG != 0:
                    if time() - Timer >= FLAG:  # 到达指定时间间隔
                        if not PAUSE:   # 没有暂停
                            IMG, IMGPATH = imgcache.next_image_func(pather, args.debug)
                            Timer = time()
                            break
                fig.canvas.flush_events()   # 等待时间发生

                # plt.pause(DELAY)
        except:
            raise

if __name__ == '__main__':
    from configtoargs import configtoargs
    args = configtoargs()
    args.debug = True
    args.mode = 'mongodb'
    args.collection = ['LIKES']
    args.time = '2'
    show_image(args)
