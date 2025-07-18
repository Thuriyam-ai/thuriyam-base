from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.database import Database as PyMongoDatabase


class MongoDBAdapter:
    """Base MongoDB adapter class"""
    username = None
    password = None
    auth_mechanism = None
    database = None
    server_selection_timeout = 5000
    _clients = {}


class MongoDBAsyncAdapter(MongoDBAdapter):
    @classmethod
    def create_db_client(cls, host: str, port: str) -> PyMongoDatabase:
        conn_string = cls._get_auth_connection_string(
            host, port, cls.username, cls.password, cls.auth_mechanism
        )
        client = AsyncIOMotorClient(
            conn_string, serverSelectionTimeoutMS=cls.server_selection_timeout
        )
        db_client = client[cls.database]
        return db_client

    @classmethod
    def _get_auth_connection_string(
        cls,
        host: str,
        port: str,
        username: str = None,
        password: str = None,
        auth_mechanism: str = None,
    ) -> str:
        # Build base connection string
        conn_string = "mongodb://"

        # Add authentication if credentials are provided
        if username and password:
            conn_string += f"{username}:{password}@"

        # Add host and port
        conn_string += f"{host}:{port}"

        # Add auth mechanism if provided
        if auth_mechanism:
            conn_string += f"/?authMechanism={auth_mechanism}"  # Added forward slash before query params

        return conn_string

    @classmethod
    def close_all(cls):
        """Close all MongoDB client connections"""
        for config_clients in cls._clients.values():
            for db_clients in config_clients.values():
                if not isinstance(db_clients, list):
                    continue
                for db_client in db_clients:
                    if isinstance(db_client, AsyncIOMotorDatabase):
                        db_client.client.close()
