MAXCACHE = 30


class PathHolder:
    def __init__(self, Method, cache=20):
        self._path_list = []
        self._id = -1
        self._next_path = Method.next_path
        self.datalength = Method.datalength
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
        if self._id == -1:
            raise Exception('PathHolder列表为空')
        if self._id == 1:
            self._id = len(self._path_list)
            path = self._path_list[self._id-1]
            return path
        else:
            self._id -= 1
            path = self._path_list[self._id - 1]
            return path

    def next_path(self):
        if self._id == len(self._path_list) or self._id == -1:
            path = self._next_path()
            self._path_list.append(path)
            self._id = len(self._path_list)
            return path
        else:
            self._id += 1
            path = self._path_list[self._id - 1]
            return path


if __name__ == '__main__':
    from mongo import MongoBuilder
    tmp = MongoBuilder()
    # tmp.clear()
    # tmp.initialize()
    path = PathHolder(tmp)
    for i in range(5):
        print(path.next_path())
    print('-'*20)
    for i in range(8):
        print(path.previous_path())
    print('-' * 20)
    for i in range(8):
        print(path.next_path())

