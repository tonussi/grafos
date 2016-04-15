import time
from time import sleep

def timeit(method):
    """To use this functionality you have to put
    @timeit just above the method you have defined
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r - %2.10f sec' % (method.__name__, te - ts))
        return result
    return timed
        