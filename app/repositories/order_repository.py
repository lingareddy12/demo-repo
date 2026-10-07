"""Data-access layer for Order."""
from sqlalchemy.orm import Session

from app.models.order import Order
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, db: Session):
        super().__init__(db, Order)

    def list_for_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Order]:
        return list(
            self.db.query(Order)
            .filter(Order.owner_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
