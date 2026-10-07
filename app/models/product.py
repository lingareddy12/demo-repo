"""Product ORM model."""
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1024), default="")
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)

    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")

    def in_stock(self) -> bool:
        """Whether the product currently has any stock available."""
        return self.stock > 0

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"<Product id={self.id} name={self.name!r}>"
