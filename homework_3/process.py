from multiprocessing import Pool, cpu_count, current_process

import time
import logging
from functools import wraps

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(processName)s %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def time_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Function {func.__name__} started")
        start = time.time()
        results = func(*args, **kwargs)
        finish = time.time()
        logger.info(
            f"Function {func.__name__} executed in {finish - start:.4f} seconds."
        )
        return results

    return wrapper


def factorize(number):
    logger.debug(f"{factorize.__name__} called. pid={current_process().pid}")
    res = []
    for i in range(1, number + 1):
        if not number % i:
            res.append(i)
    return res


@time_decorator
def sync_calc(data: tuple) -> list:
    res = []
    for num in data:
        res.append(factorize(num))
    return res


@time_decorator
def async_calc(data: tuple) -> list:
    with Pool(cpu_count()) as pool:
        return pool.map(factorize, data)


if __name__ == "__main__":
    data_factorize = (128, 255, 99999, 10651060)
    sync = sync_calc(data_factorize)
    asyn = async_calc(data_factorize)
