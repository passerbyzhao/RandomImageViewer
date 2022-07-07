MAXCACHE = 30


class PathHolder:
    """
    用于保存运行中随机出图片的路径 以保证回显功能、
    previous_path():    返回上一个图片路径
    next_path():    返回下一个随机图片路径
    get_path(id):   返回指定序号的路径
    id():   返回当前路径的序号
    """

    def __init__(self, Method, cache=20):
        self._path_list = []    # 保存随机出的路径
        self._id = -1   # 当前路径序号 从1开始计数
        self._next_path = Method.next_path  # 得到下一个随即路径
        self.datalength = Method.datalength # 总路径数量
        # 没什么用的路径缓存功能
        if self.datalength >= cache:
            self._cache = min(MAXCACHE, cache)
        elif self.datalength*0.6 >=1:
            self._cache = max(MAXCACHE, self.datalength*0.6)
        else:
            self._cache = 1
        for i in range(self._cache):
            path = self._next_path()
            self._path_list.append(path)
        self._id = 1

    def previous_path(self):
        if self._id == -1:  # 未开始的状态
            raise Exception('PathHolder列表为空')
        if self._id == 1:   # 已经回退到第一个图片路径
            path = self._path_list[0]
            return path
        else:   # 正常回退1
            self._id -= 1
            path = self._path_list[self._id - 1]
            return path

    def next_path(self):
        if self._id == len(self._path_list) or self._id == -1:  # 未初始化时或需要新增路径
            path = self._next_path()
            self._path_list.append(path)
            self._id = len(self._path_list)
            return path
        else:   # 当前路径序号未达到列表最后
            self._id += 1
            path = self._path_list[self._id - 1]
            return path

    def get_path(self, id):
        return self._path_list[id]

    @property
    def id(self):
        return self._id


if __name__ == '__main__':
    from ontime import MethodOntime
    tmp = MethodOntime()
    # tmp.clear()
    # tmp.initialize()
    path = PathHolder(tmp)
    print(path.id)
    # for i in range(5):
    #     print(path.next_path())
    # print('-'*20)
    # for i in range(8):
    #     print(path.previous_path())
    # print('-' * 20)
    # for i in range(8):
    #     print(path.next_path())

