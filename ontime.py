from random import randint
from os.path import exists

from dirtree import TreeBuilder as tree
from dirtree import TreeBuilderElse as tree2
from runtime import cruntime


class MethodOntime:
    """
    next_path():    随机返回一个有效路径 随机到无效路径时会重新随机
    """
    def __init__(self, Tree=False, target=''):
        self.Tree = Tree  # 是否自行指定用于构建文件树的目标文件
        self.target = target  # 目标文件路径
        self.dir_list = self._build_tree()  # 生成文件树
        self.datalength = len(self.dir_list)

    @cruntime
    def _build_tree(self):
        print('正在准备图片目录...', end='')
        if not self.Tree:
            dlist = tree().tree  # 获取文件树
        else:
            dlist = tree2(self.target).tree
        print('\r图片目录准备完成 ', end='')
        return dlist

    def next_path(self):
        """
        用于产出一个图片路径 由于TreeBuilder返回的文件树是真实的
        但是有可能发生运行时文件路径发生变化 因此检查路径真实性
        """

        while True:
            if self.datalength == 0:
                raise Exception('无有效图片路径')
            next_id = randint(0, self.datalength-1)     # 随机数
            path = self.dir_list[next_id]   # 获取随即路径
            if not exists(path):
                del self.dir_list[next_id]  # 路径不存在则删除这条路径
                self.datalength = len(self.dir_list)    # 重新随机
                continue
            return path


if __name__ == '__main__':
    a = MethodOntime()
    for i in range(10):
        print(a.next_path())

    print('Done')
