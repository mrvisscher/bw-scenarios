import time


def time_it(func):
    """
    For use as a wrapper to time the execution of functions using the python time library
    """
    def wrapper(*args, **kwargs):
        now = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} -- " + str(time.time() - now))
        return result
    return wrapper