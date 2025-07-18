import asyncio
from typing import Any, Dict, Optional
import redis.asyncio as redis
import pickle
from core.settings import config

DEFAULT_TIMEOUT = object()


def default_key_func(key, key_prefix, version):
    """
    Default function to generate keys.

    Construct the key used by all other methods. By default, prepend
    the `key_prefix`. KEY_FUNCTION can be used to specify an alternate
    function with custom key making behavior.
    """
    return "%s:%s:%s" % (key_prefix, version, key)


class RedisClientManager:
    _caches: Dict[str, "RedisObjectCache"] = {}

    @classmethod
    def __getitem__(cls, machine_alias: str) -> "RedisObjectCache":
        if machine_alias not in cls._caches:
            cache = RedisObjectCache.from_url(
                url=config.CACHES[machine_alias]["LOCATION"],
                socket_timeout=config.CACHES[machine_alias].get(
                    "SOCKET_TIMEOUT"
                ),
                socket_connect_timeout=config.CACHES[machine_alias].get(
                    "SOCKET_CONNECT_TIMEOUT"
                ),
            )
            key_prefix = config.CACHES[machine_alias].get("KEY_PREFIX")
            version = config.CACHES[machine_alias].get("VERSION")
            if key_prefix:
                cache.key_prefix = key_prefix
            if version:
                cache.version = version
            cls._caches[machine_alias] = cache

        return cls._caches[machine_alias]

    @classmethod
    async def close_all(cls):
        await asyncio.gather(
            *(cache.close() for cache in cls._caches.values())
        )


class RedisObjectCache(redis.Redis):
    @property
    def key_prefix(self):
        return getattr(self, "_key_prefix", "")

    @key_prefix.setter
    def key_prefix(self, value):
        setattr(self, "_key_prefix", value)

    @property
    def version(self):
        return getattr(self, "_version", 1)

    @version.setter
    def version(self, value):
        setattr(self, "_version", value)

    async def set_object(
        self,
        key: Any,
        value: Any,
        timeout: Optional[float] = DEFAULT_TIMEOUT,
        version: Optional[int] = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        """
        Persist a value to the cache, and set an optional expiration time.

        Also supports optional nx parameter. If set to True - will use redis
        setnx instead of set.
        """
        nkey = self.make_key(key, version=version)
        nvalue = self.encode(value)

        if timeout is not None:
            # Convert to milliseconds
            timeout = int(timeout * 1000)

            if timeout <= 0:
                if nx:
                    # Using negative timeouts when nx is True should
                    # not expire (in our case delete) the value if it exists.
                    # Obviously expire not existent value is noop.
                    return not await self.has_key(  # noqa: W601
                        key, version=version
                    )
                else:
                    # redis doesn't support negative timeouts in ex flags
                    # so it seems that it's better to just delete the key
                    # than to set it and than expire in a pipeline
                    return bool(await self.delete_object(key, version=version))
        return bool(await self.set(nkey, nvalue, nx=nx, px=timeout, xx=xx))

    async def get_object(self, key: Any) -> Any:
        nkey = self.make_key(key)
        nvalue = await self.get(nkey)
        if nvalue is not None:
            return self.decode(nvalue)
        return None

    async def delete_object(
        self, key: Any, version: Optional[int] = None
    ) -> bool:
        nkey = self.make_key(key, version=version)
        return await self.delete(nkey)

    async def has_key(self, key: Any, version: Optional[int] = None) -> bool:
        nkey = self.make_key(key, version=version)
        return await self.exists(nkey)

    def make_key(
        self,
        key: Any,
        version: Optional[Any] = None,
        prefix: Optional[str] = None,
    ) -> str:
        if prefix is None:
            prefix = self.key_prefix

        if version is None:
            version = self.version
        return default_key_func(key, prefix, version)

    def encode(self, value: Any) -> bytes:
        return pickle.dumps(value)

    def decode(self, value: bytes) -> Any:
        return pickle.loads(value)


caches = RedisClientManager()
