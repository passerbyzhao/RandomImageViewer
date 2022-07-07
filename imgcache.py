from PIL import Image
from threading import Thread, Condition


INITCACHE = 15  # 初始化的大小
MAXCACHE = 7    # 缓存上限
CACHE = 3   # 开启缓存的数量
CLEARCACHE = 30     # 缓存区最大数量

ImageList = []  # 缓存
ImageID = 0     # 当前访问的缓存的序号
MaxID = 0   # 到达过的最大缓存的序号
FirstID = 0     # 缓存区第一个缓存的序号

condition = Condition()


def image_list_init(path_holder):
    """
    初始化缓存
    """
    global ImageList, ImageID, MaxID
    while len(ImageList) - MaxID < INITCACHE:
        path = path_holder.next_path()
        img = Image.open(path)
        img.load()
        ImageList.append(img)


def next_image_func(path_holder, debug=False):
    """
    获取下一个缓存 如果是被删除的缓存则重新读取图片
    """
    global ImageList, ImageID, MaxID, FirstID
    with condition:
        ImageID += 1
        if ImageID - 1 < FirstID:   # 如果缓存被删除
            path = path_holder.get_path(ImageID)
            img = Image.open(path)
        else:
            img = ImageList[ImageID - 1]
            MaxID = max(MaxID, ImageID)
        if debug:
            print(path_holder.get_path(ImageID))
        # print(ImageID)
        # print('取得{}号图片'.format(ImageID))
        condition.notify()
    return img


def previous_image(path_holder):
    """
    获取上一个缓存 如果是被删除的缓存则重新读取图片
    """
    global ImageList, ImageID, MaxID, FirstID
    if ImageID == 0:    # 未初始化
        raise Exception('PathHolder列表为空')

    if ImageID == 1:
        if 0 < FirstID: # 如果缓存被删除
            path = path_holder.get_path(0)
            img = Image.open(path)
        else:
            img = ImageList[0]
        # print(ImageID)
        return img
    else:
        ImageID -= 1
        if ImageID - 1 < FirstID:   # 如果缓存被删除
            path = path_holder.get_path(ImageID)
            img = Image.open(path)
        else:
            img = ImageList[ImageID - 1]
        # print(ImageID)
        return img


class list_filler(Thread):
    """
    用于缓存图片的线程
    """
    def __init__(self, path_holder):
        Thread.__init__(self)
        self.PathHolder = path_holder

    def produce(self):
        global ImageList, ImageID, MaxID, FirstID
        with condition:
            if len(ImageList)-MaxID >= CACHE:   # 缓存已满
                condition.wait()
                # print("缓存已满 缓存长{} 最大ID为{}".format(len(ImageList), MaxID))
            if len(ImageList) - MaxID <= CACHE:     # 如果满足重新开始缓存的条件
                while len(ImageList)-MaxID < MAXCACHE:  # 缓存至MAXCACHE
                    path = self.PathHolder.next_path()
                    img = Image.open(path)
                    img.load()
                    ImageList.append(img)
                if len(ImageList) > CLEARCACHE:     # 如果缓存区超过最大大小 删除最早的缓存
                    while len(ImageList)-FirstID > CLEARCACHE:
                        ImageList[FirstID] = ''
                        FirstID += 1

            # print("已缓存{} 缓存区{}".format(len(ImageList), len(ImageList)-MaxID))
            condition.notify()

    def run(self):
        while True:
            self.produce()


if __name__ == '__main__':

    print('Done')
