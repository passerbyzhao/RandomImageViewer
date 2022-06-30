import re
from random import randint
from os.path import exists

import pymongo

from dirtree import TreeBuilder as tree
from runtime import cruntime


class MethodMonge:
    """
    initialize():   初始化数据库 将原来的数据全部清除再重新添加
    update():   不改动原有数据 只添加新增条目
    clear():    清除数据库中的所有数据
    next_path():    随机返回一个有效路径 随机到无效路径时会从数据库中删除该路径并重新随机
    """
    def __init__(self, collection):
        self.ri = collection
        self.compile = re.compile(r'.*?')
        self.datalength = self.ri.count_documents({})

    @cruntime
    def initialize(self):
        print('数据库准备中...', end='')
        self.ri.drop()
        dir_list = tree().tree
        for path in dir_list:
            self.ri.insert_one({'path': path})
        self.datalength = self.ri.count_documents({})
        print('\r数据库准备就绪 共{}个路径 '.format(self.datalength), end='')

    @cruntime
    def update(self):
        print('数据库准备中...', end='')
        dir_list = tree().tree
        for path in dir_list:
            if self.ri.find_one({'path': path}) is None:
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
        while True:
            if self.datalength == 0:
                raise Exception('无有效图片路径')
            next_id = randint(0, self.datalength-1)
            path = self.ri.find_one({'path': self.compile}, skip=next_id)['path']
            if not exists(path):
                self.ri.delete_one({'path': path})
                self.datalength = self.ri.count_documents({})
                continue
            return path


class MongoBuilder(MethodMonge):
    def __init__(self, client='mongodb://localhost:27017/', db='RandomImage', collection='ImagePath'):
        client = pymongo.MongoClient(client)
        db = client[db]
        ri = db[collection]
        MethodMonge.__init__(self, ri)

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
    u.clear()
    # re.findall(r'\.([a-zA-Z0-9]+)$', a)[-1]
