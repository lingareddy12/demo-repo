"""Business logic for product catalog management."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.exceptions import NotFoundError


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def create(self, payload: ProductCreate) -> Product:
        product = Product(**payload.model_dump())
        return self.repo.create(product)

    def get(self, product_id: int) -> Product:
        product = self.repo.get(product_id)
        if product is None:
            raise NotFoundError("Product", product_id)
        return product

    def list(self, skip: int = 0, limit: int = 100) -> list[Product]:
        return self.repo.list(skip=skip, limit=limit)

    def search(self, query: str) -> list[Product]:
        return self.repo.search_by_name(query)

    def update(self, product_id: int, payload: ProductUpdate) -> Product:
        product = self.get(product_id)
        updates = payload.model_dump(exclude_unset=True)
        return self.repo.update(product, updates)

    def delete(self, product_id: int) -> None:
        product = self.get(product_id)
        self.repo.delete(product)

    def adjust_stock(self, product_id: int, delta: int) -> Product:
        """Increase or decrease stock (delta may be negative)."""
        product = self.get(product_id)
        product.stock = max(0, product.stock + delta)
        self.repo.db.commit()
        self.repo.db.refresh(product)
        return product
