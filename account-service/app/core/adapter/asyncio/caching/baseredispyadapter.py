from typing import Optional
from redis.asyncio import Redis
from jobnotification.adapter.asyncio.caching.client import caches
from core.settings import config as settings


class BaseRedisPyAsyncCacheHandler:
    def __init__(
        self,
        key: str,
        timeout_in_seconds: Optional[int] = None,
        machine_alias: str = "default",
    ):
        self.machine_alias = machine_alias
        self.key = self.__get_key_with_prefix(key)
        self.timeout = timeout_in_seconds
        self._adapter: Redis = None

    async def init(self):
        if not hasattr("self", "_adapter"):
            self._adapter = caches[self.machine_alias]
        return self

    @property
    def adapter(self):
        if self._adapter is None:
            raise AttributeError(
                f"{type(self).__name__}: `_adapter` is not set. Call `init()` method first"
            )
        return self._adapter

    def get_configuration(self):
        raise NotImplementedError

    def __get_key_with_prefix(self, key):
        prefix = settings.CACHES[self.machine_alias].get("KEY_PREFIX")
        if prefix:
            return prefix + ":" + key
        return key

    async def exists(self):
        """Returns a boolean indicating if the key exist in cache"""
        return bool(await self.adapter.exists(self.key))

    async def invalidate_cache(self):
        """Deletes the key in cache"""
        return await self.adapter.delete(self.key)

    # Sorted Set Methods

    async def zadd(
        self, content: dict, nx=False, xx=False, ch=False, incr=False
    ):
        result = await self.adapter.zadd(
            self.key, content, nx=nx, xx=xx, ch=ch, incr=incr
        )
        if self.timeout:
            await self.adapter.expire(self.key, self.timeout)
        return result

    async def zrange(
        self, start, end, desc=False, withscores=False, score_cast_func=float
    ):
        return await self.adapter.zrange(
            self.key,
            start,
            end,
            desc=desc,
            withscores=withscores,
            score_cast_func=score_cast_func,
        )

    async def zrangebyscore(
        self,
        min,
        max,
        start=None,
        num=None,
        withscores=False,
        score_cast_func=float,
    ):
        return await self.adapter.zrangebyscore(
            self.key,
            min,
            max,
            start=start,
            num=num,
            withscores=withscores,
            score_cast_func=score_cast_func,
        )

    async def zscore(self, value):
        return await self.adapter.zscore(self.key, value)

    async def zincrby(self, value, amount: float):
        result = await self.adapter.zincrby(self.key, amount, value)
        if self.timeout:
            await self.adapter.expire(self.key, self.timeout)
        return result

    async def zrank(self, value):
        return await self.adapter.zrank(self.key, value)

    async def zrem(self, *values):
        return await self.adapter.zrem(self.key, *values)

    # Set Methods

    async def sadd(self, *values):
        result = await self.adapter.sadd(self.key, *values)
        if self.timeout:
            await self.adapter.expire(self.key, self.timeout)
        return result

    async def smembers(self):
        return await self.adapter.smembers(self.key)

    async def scard(self):
        return await self.adapter.scard(self.key)

    async def sismember(self, value):
        return await self.adapter.sismember(self.key, value)

    async def srem(self, *values):
        return await self.adapter.srem(self.key, *values)

    # Redis Hash Methods

    async def hset(self, field, value):
        return await self.adapter.hset(self.key, field, value)

    async def hsetnx(self, field, value):
        return await self.adapter.hsetnx(self.key, field, value)

    async def hget(self, field):
        return await self.adapter.hget(self.key, field)

    async def hgetall(self):
        return await self.adapter.hgetall(self.key)

    async def hrem(self, *fields):
        return await self.adapter.hdel(self.key, *fields)

    async def hexist(self, field):
        return await self.adapter.hexists(self.key, field)

    async def hkeys(self):
        return await self.adapter.hkeys(self.key)

    async def hvals(self):
        return await self.adapter.hvals(self.key)

    async def hincrby(self, field, amount: int):
        return await self.adapter.hincrby(self.key, field, amount)

    async def hincrbyfloat(self, field, amount: float):
        return await self.adapter.hincrbyfloat(self.key, field, amount)

    # Redis List Methods

    async def lpush(self, *values):
        return await self.adapter.lpush(self.key, *values)

    async def rpush(self, *values):
        return await self.adapter.rpush(self.key, *values)

    async def llen(self) -> int:
        return await self.adapter.llen(self.key)

    async def lindex(self, index: int):
        return await self.adapter.lindex(self.key, index)

    async def lrange(self, start: int = 0, end: int = -1):
        return await self.adapter.lrange(self.key, start=start, end=end)

    async def lpop(self, count: int = 1):
        return await self.adapter.lpop(self.key, count=count)

    async def rpop(self, count: int = 1):
        return await self.adapter.rpop(self.key, count=count)
