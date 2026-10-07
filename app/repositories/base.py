"""Generic repository providing common CRUD operations over a SQLAlchemy model."""
from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Thin data-access layer around a single SQLAlchemy model.

    Concrete repositories subclass this and add model-specific queries
    (e.g. `get_by_email`) on top of the generic operations here.
    """

    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def get(self, id_: int) -> ModelType | None:
        return self.db.get(self.model, id_)

    def list(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return list(self.db.query(self.model).offset(skip).limit(limit).all())

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType, updates: dict) -> ModelType:
        for field, value in updates.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.commit()
