from jobnotification.adapter.asyncio.caching.baseredispyadapter import (
    BaseRedisPyAsyncCacheHandler,
)


class ShardedRedisPyAsyncCacheHandler(BaseRedisPyAsyncCacheHandler):
    def __init__(
        self, key, timeout_in_seconds, machine_alias, shard_identifier
    ):
        if type(machine_alias) == list:
            shard_index = int(shard_identifier) % len(machine_alias)
            shard_alias = machine_alias[shard_index]
        else:
            shard_alias = machine_alias

        super().__init__(
            key,
            timeout_in_seconds=timeout_in_seconds,
            machine_alias=shard_alias,
        )
