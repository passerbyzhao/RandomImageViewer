import time

def runtime(func):
    def _warp(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        running_time = time.time() - start_time
        print('耗时%.6fs'%running_time)
        return result
    return _warp

def cruntime(func):
    def _warp(self, *args, **kwargs):
        start_time = time.time()
        result = func(self, *args, **kwargs)
        running_time = time.time() - start_time
        print('耗时%.6fs'%running_time)
        return result
    return _warp