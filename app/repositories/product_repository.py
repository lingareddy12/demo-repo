"""Data-access layer for Product."""
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(db, Product)

    def search_by_name(self, query: str, limit: int = 50) -> list[Product]:
        return list(
            self.db.query(Product)
            .filter(Product.name.ilike(f"%{query}%"))
            .limit(limit)
            .all()
        )
