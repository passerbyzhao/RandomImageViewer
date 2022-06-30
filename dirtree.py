from os.path import exists
from pathlib import Path

ImageType = ('jpg', 'png', 'jpeg', 'bmp', 'tif', 'tga', 'eps', 'psd',
             'JPG', 'PNG', 'JPEG', 'BMP', 'TIF', 'TGA', 'EPS', 'PSD')


class TreeBuilder:
    """
    _read_directory():  从指定文件中读取目录
    _getall():  用于遍历目录下所有文件的递归函数
    """
    def __init__(self):
        _dir_list = self._read_directory()
        self.tree = []
        for directory in _dir_list:
            path = Path(directory)
            self._getall(path)
        if len(self.tree) == 0:
            raise Exception('目录下无图片文件')

    def _read_directory(self):
        if not exists('目录.txt'):
            with open('目录.txt', 'w', encoding='utf-8') as f:
                f.close()
            raise Exception('未指定图片目录，请将图片目录放到程序根目录下的\'目录.txt\'内。')
        _dir_list = []
        with open('目录.txt', 'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if line == '':
                    break
                line = line.strip()
                if line not in _dir_list and line != '':
                    _dir_list.append(line)
        if _dir_list == [] or _dir_list == ['']:
            raise Exception('未指定图片目录，请将图片目录放到程序根目录下的\'目录.txt\'内。')
        for directory in _dir_list:
            if not exists(directory):
                raise Exception('图片目录\'{}\'错误。一行只能放一个目录。'.format(directory))
        return _dir_list

    def _getall(self, path):
        if path.is_file():
            path = str(path)
            if path.endswith(ImageType):
                self.tree.append(path)
        elif path.is_dir():
            for item in path.iterdir():
                self._getall(item)
        else:
            raise Exception('非文件非目录错误，不应输出：{}'.format(str(path)))

class TreeBuilderElse:
    """
    _read_directory():  从指定文件中读取目录
    _getall():  用于遍历目录下所有文件的递归函数
    """
    def __init__(self, filedir='目录.txt'):
        self._filedir = filedir
        _dir_list = self._read_directory()
        self.tree = []
        for directory in _dir_list:
            path = Path(directory)
            self._getall(path)
        if len(self.tree) == 0:
            raise Exception('目录下无图片文件')

    def _read_directory(self):
        if not exists(self._filedir):
            raise Exception('图片目录文件不存在')
        _dir_list = []
        with open(self._filedir, 'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if line == '':
                    break
                line = line.strip()
                if line not in _dir_list and line != '':
                    _dir_list.append(line)
        if _dir_list == [] or _dir_list == ['']:
            raise Exception('未指定图片目录')
        for directory in _dir_list:
            if not exists(directory):
                raise Exception('图片目录\'{}\'错误。一行只能放一个目录。'.format(directory))
        return _dir_list

    def _getall(self, path):
        if path.is_file():
            path = str(path)
            if path.endswith(ImageType):
                self.tree.append(path)
        elif path.is_dir():
            for item in path.iterdir():
                self._getall(item)
        else:
            raise Exception('非文件非目录错误，不应输出：{}'.format(str(path)))


if __name__ == '__main__':
    tree = TreeBuilder()
    dir_list = tree.tree
    print(tree.tree[0:10])
    print(len(tree.tree))
