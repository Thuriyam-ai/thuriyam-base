from datadog import DogStatsd


class StatsDDefaultClient:
    _initialized = False
    _client = None

    @classmethod
    def init_client(cls, client: DogStatsd):
        cls._client = client
        cls._initialized = True

    def __getattr__(self, name):
        if not self._initialized:
            raise AttributeError(
                f"Client has not been initialized. Cannot access '{name}'."
            )
        return getattr(self._client, name)


class StatsdConfigurationMissingException(Exception):
    def __str__(self):
        return "`host` and `port` configuration is cannot be null"


class StatsdClientManager:
    def __init__(self, host: str, port: int, service_name: str, prefix: str):
        self.host = host
        self.port = port
        self.service_name = service_name
        self.prefix = prefix

    def init_default_client(self):
        # Should be called only once when the app starts
        client = self.get_client()
        StatsDDefaultClient.init_client(client)

    def get_client(self):
        if not self.host or not self.port:
            raise StatsdConfigurationMissingException()

        constant_tags = []

        if self.service_name:
            constant_tags.append(f"service:{self.service_name}")

        return DogStatsd(
            host=self.host,
            port=self.port,
            namespace=self.prefix,
            constant_tags=constant_tags,
        )


client: DogStatsd = StatsDDefaultClient()
