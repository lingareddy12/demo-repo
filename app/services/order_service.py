"""Business logic for placing and managing orders.

This service coordinates across the Product and Order repositories,
which is the kind of multi-hop, cross-module relationship a codebase
graph is useful for surfacing (OrderService -> ProductService -> Product).
"""
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate
from app.services.product_service import ProductService
from app.utils.exceptions import InsufficientStockError, NotFoundError


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrderRepository(db)
        self.products = ProductService(db)

    def place_order(self, user_id: int, payload: OrderCreate) -> Order:
        """Validate stock, decrement it, and persist a new order with line items."""
        order = Order(owner_id=user_id)

        for item in payload.items:
            product = self.products.get(item.product_id)
            if product.stock < item.quantity:
                raise InsufficientStockError(
                    product_id=product.id, requested=item.quantity, available=product.stock
                )
            order.items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=product.price,
                )
            )
            self.products.adjust_stock(product.id, -item.quantity)

        return self.repo.create(order)

    def get(self, order_id: int) -> Order:
        order = self.repo.get(order_id)
        if order is None:
            raise NotFoundError("Order", order_id)
        return order

    def list_for_user(self, user_id: int) -> list[Order]:
        return self.repo.list_for_user(user_id)

    def mark_paid(self, order_id: int) -> Order:
        order = self.get(order_id)
        order.mark_paid()
        self.db.commit()
        self.db.refresh(order)
        return order
