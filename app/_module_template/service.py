from datetime import timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.settings import get_config
from core.database import get_db
from core.base.model import ModelBuilder, Operation
from core.security.auth import verify_password, get_password_hash
from core.security.jwt import create_access_token
from __MODULE_NAME__.model import __CLASS_NAME__
from __MODULE_NAME__.schema import __CLASS_NAME__Create, __CLASS_NAME__Update
from __MODULE_NAME__.repository import __CLASS_NAME__Repository

settings = get_config()

class __CLASS_NAME__Service:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = __CLASS_NAME__Repository(db)

    def create___SINGULAR_VAR_NAME__(self, input: __CLASS_NAME__Create) -> __CLASS_NAME__:
        # TODO: Validate user input

        # Building a model using the ModelBuilder instead of the existing build function.
        __SINGULAR_VAR_NAME__ = ModelBuilder.for_model(__CLASS_NAME__).with_operation(
            Operation.CREATE
        ).with_attributes(
            input.model_dump(exclude_unset=True)
        ).build()

        return self.repository.save(__SINGULAR_VAR_NAME__)

    def update(self, id: str, input: __CLASS_NAME__Update) -> Optional[__CLASS_NAME__]:
        # TODO: Add validation for the input

        update_data = input.model_dump(exclude_unset=True)

        return self.repository.update(id, update_data)

    def delete(self, id: str) -> bool:
        # TODO: Add validation for the input
        return self.repository.delete(id)

    def list(self, skip: int = 0, limit: int = 100) -> list[__CLASS_NAME__]:
        return self.repository.find_all(skip=skip, limit=limit) 