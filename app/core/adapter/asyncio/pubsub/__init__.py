import asyncio
import time
import logging
from typing import Optional
from wikafkaadapter.kafka.baseconsumer import (
    BaseConsumer,
    ErrorType,
    StatsDMonitoring,
    KafkaCosumerMonitoring,
)

try:
    from django.db import OperationalError as DjangoOperationalError

    is_django_imported = True
except ImportError:
    is_django_imported = False
    DjangoOperationalError = None

from jobnotification.adapter.statsd import client as statsd_client

logger = logging.getLogger("wi.event.kafka.log")


class BaseAsyncConsumer(BaseConsumer):
    """
    Supports handling of async `handle_message` and `handle_operation_failure` methods.

    Even though `handle_message` can be async but still each message will be processed sequentially
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._event_loop = None

    def _get_event_loop(self) -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
        return loop

    @property
    def event_loop(self) -> asyncio.AbstractEventLoop:
        if self._event_loop is None:
            self._event_loop = self._get_event_loop()
        return self._event_loop

    def consume(self):
        while True:
            try:
                start_ts = time.time()
                msg = self.consumer.poll(1.0)
                self.push_polling_metric(msg, start_ts)

                if msg:
                    start_ts = time.time()
                    message = self.process_message(msg)
                    # close_old_db_connections() is maintenance code that is run
                    # to keep the consumer up and running on k8s
                    # it closes old db connections(set by MAX_AGE in db settings).
                    # Django closes connections by default on every new request
                    # since we do not have any api request here, we will have to manually run the code
                    self.close_old_db_connections()

                    if asyncio.iscoroutinefunction(self.handle_message):
                        self.event_loop.run_until_complete(
                            self.handle_message(message=message)
                        )
                    else:
                        self.handle_message(message=message)

                    self.push_message_processing_metric(message, start_ts)

            except Exception as e:
                self.push_error_metric(e, ErrorType.UNHANDLED)
                if is_django_imported and isinstance(
                    e, DjangoOperationalError
                ):
                    # this is a db related error and not a kafka related error
                    # owing to the fact that it is a db related error, it is assumed that msg has
                    # been successfully polled from the kafka-broker
                    if asyncio.iscoroutinefunction(
                        self.handle_operational_errors
                    ):
                        self.event_loop.run_until_complete(
                            self.handle_operational_errors()
                        )
                    else:
                        self.handle_operational_errors()
                    # re-raise the error therefore terminating the application
                    raise
                else:
                    logger.error(
                        f"Error in Consume of" f" {self.__class__.__name__}.",
                        exc_info=True,
                    )

    def get_monitoring_client(
        self, **kwargs
    ) -> Optional[KafkaCosumerMonitoring]:
        """Returns `monitoring_client` for pushing consumer metrics"""
        # By default StatsD is used for monitoring | For any other client override this method in subclass
        if not self.monitoring_enabled:
            logger.warning(
                f"{self.__class__.__name__} | Monitoring is disabled"
            )
            return

        logger.info(f"{self.__class__.__name__} | Monitoring is enabled")
        monitoring_client = StatsDMonitoring(statsd_client)
        return monitoring_client

    def close_old_db_connections(self):
        pass
