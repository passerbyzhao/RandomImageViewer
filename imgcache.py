import time
from PIL import Image
from threading import Thread, Condition

from matplotlib import pyplot as plt


INITCACHE = 15
MAXCACHE = 7
CACHE = 3
CLEARCACHE = 30

ImageList = []
ImageID = 0
MaxID = 0
condition = Condition()
FirstID = 0


def image_list_init(path_holder):
    global ImageList, ImageID, MaxID
    while len(ImageList) - MaxID < INITCACHE:
        path = path_holder.next_path()
        img = Image.open(path)
        img.load()
        ImageList.append(img)


class next_image(Thread):
    def __init__(self, path_holder):
        Thread.__init__(self)
        self.PathHolder = path_holder

    def next(self):
        global ImageList, ImageID, MaxID, FirstID
        condition.acquire()
        ImageID += 1
        if ImageID-1 < FirstID:
            path = self.PathHolder.get_path(ImageID)
            img = Image.open(path)
        else:
            img = ImageList[ImageID - 1]
            MaxID = max(MaxID, ImageID)
        # print(ImageID)
        # print('取得{}号图片'.format(ImageID))
        condition.notify()
        condition.release()
        return img

    def run(self):
        img =self.next()
        return img


def previous_image(path_holder):
    global ImageList, ImageID, MaxID, FirstID
    if ImageID == 0:
        raise Exception('PathHolder列表为空')

    if ImageID == 1:
        if 0 < FirstID:
            path = path_holder.get_path(0)
            img = Image.open(path)
        else:
            img = ImageList[0]
        # print(ImageID)
        return img
    else:
        ImageID -= 1
        if ImageID - 1 < FirstID:
            path = path_holder.get_path(ImageID)
            img = Image.open(path)
        else:
            img = ImageList[ImageID - 1]
        # print(ImageID)
        return img


class list_filler(Thread):
    def __init__(self, path_holder):
        Thread.__init__(self)
        self.PathHolder = path_holder

    def produce(self):
        global ImageList, ImageID, MaxID, FirstID
        condition.acquire()
        if len(ImageList)-MaxID >= CACHE:
            condition.wait()
            # print("缓存已满 缓存长{} 最大ID为{}".format(len(ImageList), MaxID))
        if len(ImageList) - MaxID <= CACHE:
            while len(ImageList)-MaxID < MAXCACHE:
                path = self.PathHolder.next_path()
                img = Image.open(path)
                img.load()
                ImageList.append(img)
            if len(ImageList) > CLEARCACHE:
                while len(ImageList)-FirstID > CLEARCACHE:
                    ImageList[FirstID] = ''
                    FirstID += 1

        # print("已缓存{} 缓存区{}".format(len(ImageList), len(ImageList)-MaxID))
        condition.notify()
        condition.release()

    def run(self):
        while True:
            self.produce()


if __name__ == '__main__':

    method = Method()
    path_holder = PathHolder(method)
    Timer = time.time()
    image_list_init(path_holder)
    lock = list_filler(path_holder)
    lock.daemon = True
    lock.start()
    # lock.join()

    print(time.time()-Timer)
    # time.sleep(2)
    # for i in range(5):
    #     tmp = next_image(path_holder).run()
    #     print(tmp)
    #     time.sleep(1)


    plt.rcParams['toolbar'] = 'None'
    plt.rcParams['keymap.quit'] = ['escape', 'q', 'ctrl+q']
    # plt.axis('off')   # USELESS
    fig = plt.figure(num=42)
    fig.set_tight_layout('pad')
    fig.set_facecolor('k')
    ax = fig.subplots()
    Timer = time.time()
    for i in range(10):

        ax.clear()
        ax.axis('off')
        img = next_image(path_holder).run()
        ax.imshow(img, interpolation='none', filternorm=False, resample=False)

    print(time.time()-Timer)


