from jobnotification.adapter.asyncio.caching.client import caches


class AsyncRedisCacheAdapter:
    @staticmethod
    async def set(key, value, timeout=None, machine_alias="default"):
        _key = key
        _timeout = timeout or 60 * 1
        cache = caches[machine_alias]
        return await cache.set_object(_key, value, timeout=_timeout)

    @staticmethod
    async def get(key, machine_alias="default"):
        cache = caches[machine_alias]
        return await cache.get_object(key)  # Async get

    @staticmethod
    async def delete(key, machine_alias="default"):
        cache = caches[machine_alias]
        return await cache.delete_object(key)  # Async delete
