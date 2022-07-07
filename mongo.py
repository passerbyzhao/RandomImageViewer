import re
from random import randint
from os.path import exists

import pymongo

from dirtree import TreeBuilder as tree
from dirtree import TreeBuilderElse as tree2
from runtime import cruntime


class MethodMonge:
    """
    initialize():   初始化数据库 将原来的数据全部清除再重新添加
    update():   不改动原有数据 只添加新增条目
    clear():    清除数据库中的所有数据
    next_path():    随机返回一个有效路径 随机到无效路径时会从数据库中删除该路径并重新随机
    """

    def __init__(self, collection, Tree=False, target=''):
        self.ri = collection
        self.Tree = Tree    # 是否自行指定用于构建文件树的目标文件
        self.target = target    # 目标文件路径
        self.compile = re.compile(r'.*?')   # 用于匹配任意字符
        self.datalength = self.ri.count_documents({})   # 数据库中数据条数

    @cruntime
    def initialize(self):   # 初始化数据库
        print('数据库准备中...', end='')
        self.ri.drop()      # 删掉所有数据
        if not self.Tree:
            dir_list = tree().tree  # 获取文件树
        else:
            dir_list = tree2(self.target).tree
        for path in dir_list:
            self.ri.insert_one({'path': path})  # 逐条更新数据库
        self.datalength = self.ri.count_documents({})   # 更新数据条数
        print('\r数据库准备就绪 共{}个路径 '.format(self.datalength), end='')

    @cruntime
    def update(self):
        print('数据库准备中...', end='')
        if not self.Tree:
            dir_list = tree().tree  # 获取文件树
        else:
            dir_list = tree2(self.target).tree
        for path in dir_list:
            if self.ri.find_one({'path': path}) is None:    # 如果数据库中不存在该数据 则更新数据
                self.ri.insert_one([])
        self.datalength = self.ri.count_documents({})
        print('\r数据库更新完毕 共{}个路径 '.format(self.datalength), end='')

    @cruntime
    def clear(self):
        self.ri.drop()
        self.datalength = self.ri.count_documents({})
        if self.datalength == 0:
            print('MongoDB数据清除完毕 ', end='')
        else:
            print('\033[31mMongoDB数据清除失败\033[0m ', end='')

    def next_path(self):
        """
        用于产出一个图片路径 由于TreeBuilder返回的文件树是真实的 因此插入数据时不检查路径真实性
        但是读取数据时不确定路径是否发生变动 因此需要重新检验路径真实性
        """

        while True:
            if self.datalength == 0:
                raise Exception('无有效图片路径')
            next_id = randint(0, self.datalength-1)     # 随机跳过数据的数量
            path = self.ri.find_one({'path': self.compile}, skip=next_id)['path']   # 读取随机路径
            if not exists(path):    # 判断路径真实性
                self.ri.delete_one({'path': path})  # 不存在就删除该路径
                self.datalength = self.ri.count_documents({})   # 更新数据数量
                continue    # 重新随机
            return path


class MongoBuilder(MethodMonge):
    """
    通过参数连接到指定数据库 并返回相应的数据库表类
    """
    def __init__(self, client='mongodb://localhost:27017/', db='RandomImage', collection='ImagePath', Tree=False, target=''):
        client = pymongo.MongoClient(client)
        db = client[db]
        ri = db[collection]
        MethodMonge.__init__(self, ri, Tree=Tree, target=target)


if __name__ == '__main__':
    # client = pymongo.MongoClient('localhost', 27017)
    # db = client.RandomImage
    # riri = db.ImagePath
    # u = MethodMonge(riri)
    u = MongoBuilder()

    u.initialize()
    for i in range(10):
        v = u.next_path()
        print(v)

    print('Done')
