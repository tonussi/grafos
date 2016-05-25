import time, threading

def timeit(method):
    """To use this functionality you have to put
    @timeit just above the method you have defined
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        slave = threading.current_thread()
        print('Thread id={%i} name={%s} - %r - %2.10f sec\n' % (slave.tid, slave.name, method.__name__, te - ts))
        return result
    return timed
