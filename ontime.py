from random import randint
from os.path import exists

from dirtree import TreeBuilder as tree
from runtime import cruntime


class MethodOntime:
    """
    next_path():    随机返回一个有效路径 随机到无效路径时会重新随机
    """
    def __init__(self):
        self.dir_list = self._build_tree()
        self.datalength = len(self.dir_list)

    @cruntime
    def _build_tree(self):
        print('正在准备图片目录...', end='')
        dlist = tree().tree
        print('\r图片目录准备完成 ', end='')
        return dlist

    def next_path(self):
        while True:
            if self.datalength == 0:
                raise Exception('无有效图片路径')
            next_id = randint(0, self.datalength-1)
            path = self.dir_list[next_id]
            if not exists(path):
                del self.dir_list[next_id]
                self.datalength = len(self.dir_list)
                continue
            return path


if __name__ == '__main__':
    a = MethodOntime()
    for i in  range(10):
        print(a.next_path())

    print('Done')