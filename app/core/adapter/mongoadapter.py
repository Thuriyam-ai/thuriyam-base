from core.settings import config as settings

from jobnotification.adapter.asyncio.mongo.mongodbadapter import (
    MongoDBAsyncAdapter,
)


JOB_NOTIFICATION_MONGO = settings.NOSQL_DATABASES["mongodb"]


class JobNotificationMongoAdapter(MongoDBAsyncAdapter):
    config_name = "mongodb_job_notification"
    host: str = JOB_NOTIFICATION_MONGO["HOST"]
    port: str = JOB_NOTIFICATION_MONGO["PORT"]
    read_replicas = JOB_NOTIFICATION_MONGO["READ_REPLICAS"]
    database: str = JOB_NOTIFICATION_MONGO["NAME"]
    should_authenticate: bool = JOB_NOTIFICATION_MONGO["SHOULD_AUTHENTICATE"]
    username: str = JOB_NOTIFICATION_MONGO["USERNAME"]
    password: str = JOB_NOTIFICATION_MONGO["PASSWORD"]
    auth_mechanism: str = "SCRAM-SHA-1" if should_authenticate else None
