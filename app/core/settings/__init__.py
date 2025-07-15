import os
from typing import Type
from .base import BaseConfig

import logging

logger = logging.getLogger(__name__)

_registered_configs = {}

def register(flavour: str, config_class: Type[BaseConfig]):
    logger.info(f"Registering config for flavour: {flavour}")
    _registered_configs[flavour] = config_class

class _ConfigFactory:
    def get(flavour: str) -> BaseConfig:
        return _registered_configs[flavour]()

flavour: str = os.environ.setdefault("FLAVOUR", "dev")

config: BaseConfig = None

def get_config() -> BaseConfig:
    global config
    if config is None:
        config = _ConfigFactory.get(flavour)
    return config
