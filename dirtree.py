from os.path import exists, getsize
from pathlib import Path


ImageType = ('jpg', 'png', 'jpeg', 'bmp', 'tif', 'tga', 'eps', 'psd',)
MINFILESIZE = 100   # 最小文件大小 100B


class TreeBuilder:
    """
    _read_directory():  从指定文件中读取目录
    _getall():  用于遍历目录下所有文件的递归函数
    """

    def __init__(self):
        _dir_list = self._read_directory()  # 从目标文件读取目录（可能有多个）
        self.tree = []  # 用于存放文件树
        for directory in _dir_list:     # 构造文件树
            path = Path(directory)
            self._getall(path)
        if len(self.tree) == 0:     # 目录下无图片文件时引发异常
            raise Exception('目录下无图片文件')

    def _read_directory(self):
        if not exists('目录.txt'):    # 首先判断目标文件真实性 不存在会创建目标文件
            with open('目录.txt', 'w', encoding='utf-8') as f:    # 创建空目标文件
                f.close()
            raise Exception('未指定图片目录，请将图片目录放到程序根目录下的\'目录.txt\'内。')
        _dir_list = []  # 目标文件中的目录暂存列表
        with open('目录.txt', 'r', encoding='utf-8') as f:
            while True:     # 循环读取每行中的文本
                line = f.readline()
                if line == '':  # 到达文件末尾
                    break
                line = line.strip()
                if line not in _dir_list and line != '':    # 加入不重复且不为空的目录
                    _dir_list.append(line)
        if _dir_list == [] or _dir_list == ['']:     # 不存在有效目录
            raise Exception('未指定图片目录，请将图片目录放到程序根目录下的\'目录.txt\'内。')
        for directory in _dir_list:     # 检查目录真实性
            if not exists(directory):
                raise Exception('图片目录\'{}\'错误。目录不存在或有一行有多个目录。'.format(directory))
        return _dir_list

    def _getall(self, path):
        if path.is_file():      # 如果是文件
            path = str(path)
            if path.lower().endswith(ImageType):    # 判断是不是图片
                if getsize(path) > MINFILESIZE:     # 判断文件大小
                    self.tree.append(path)
        elif path.is_dir():     # 如果是目录 进行递归
            for item in path.iterdir():
                self._getall(item)
        else:   # 应该是没用的？
            raise Exception('非文件非目录错误，不应输出：{}'.format(str(path)))


class TreeBuilderElse:
    """
    用于从指定目标文件中读取目录
    _read_directory():  从指定文件中读取目录
    _getall():  用于遍历目录下所有文件的递归函数
    """

    def __init__(self, filedir='目录.txt'):
        self._filedir = filedir     # 目标文件路径
        _dir_list = self._read_directory()  # 从目标文件读取目录（可能有多个）
        self.tree = []  # 用于存放文件树
        for directory in _dir_list:     # 构造文件树
            path = Path(directory)
            self._getall(path)
        if len(self.tree) == 0:     # 目录下无图片文件时引发异常
            raise Exception('目录下无图片文件')
        self._filedir = filedir

    def _read_directory(self):
        if not exists(self._filedir):    # 首先判断目标文件真实性
            raise Exception('图片目录文件{}不存在'.format(self._filedir))
        _dir_list = []  # 目标文件中的目录暂存列表
        with open(self._filedir, 'r', encoding='utf-8') as f:
            while True:     # 循环读取每行中的文本
                line = f.readline()
                if line == '':  # 到达文件末尾
                    break
                line = line.strip()
                if line not in _dir_list and line != '':    # 加入不重复且不为空的目录
                    _dir_list.append(line)
        if _dir_list == [] or _dir_list == ['']:     # 不存在有效目录
            raise Exception('未指定图片目录')
        for directory in _dir_list:     # 检查目录真实性
            if not exists(directory):
                raise Exception('图片目录\'{}\'错误。目录不存在或有一行有多个目录。'.format(directory))
        return _dir_list

    def _getall(self, path):
        if path.is_file():      # 如果是文件
            path = str(path)
            if path.lower().endswith(ImageType):    # 判断是不是图片
                if getsize(path) > MINFILESIZE:  # 判断文件大小
                    self.tree.append(path)
        elif path.is_dir():     # 如果是目录 进行递归
            for item in path.iterdir():
                self._getall(item)
        else:   # 应该是没用的？
            raise Exception('非文件非目录错误，不应输出：{}'.format(str(path)))


if __name__ == '__main__':
    tree = TreeBuilder()
    dir_list = tree.tree
    print(tree.tree[0:10])
    print(len(tree.tree))

    print('Done')
