import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

# r.set('key', 'value')

# res = r.get('key')


@cache
def f(x):
    print("Function call f({x})")
    return x


if __name__ == "__main__":
    print(f(2))
    print(f(3))
