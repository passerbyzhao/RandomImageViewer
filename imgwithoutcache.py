from functools import lru_cache

from PIL import Image


class ImgCache:
    def __init__(self):
        self.ImageID = 0
        self.ImageList = []
        self.MaxID = 0
        self.__tmppic = ''

    def next_image_func(self, path_holder, debug=False):
        """
        获取下一个缓存 如果是被删除的缓存则重新读取图片
        """
        self.ImageID += 1
        if self.ImageID > self.MaxID:
            path = path_holder.next_path()
            self.MaxID = self.ImageID
        else:
            path = path_holder.get_path(self.ImageID)
        img = Image.open(path)
        if debug:
            print(path_holder.get_path(self.ImageID))
        return img, path

    def previous_image(self, path_holder):
        """
        获取上一个缓存 如果是被删除的缓存则重新读取图片
        """
        if self.ImageID == 0:    # 未初始化
            raise Exception('PathHolder列表为空')

        if self.ImageID == 1:
            path = path_holder.get_path(0)
            img = Image.open(path)
        else:
            self.ImageID -= 1
            path = path_holder.get_path(self.ImageID)
            img = Image.open(path)
        return img, path

    @property
    @lru_cache(20)
    def img(self):
        return self.__tmppic

    @img.setter
    def img(self, img):
        img.load()
        self.__tmppic = img




if __name__ == '__main__':

    print('Done')
