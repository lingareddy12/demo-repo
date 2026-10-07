"""Product catalog endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductService
from app.utils.exceptions import NotFoundError

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(
    q: str | None = Query(default=None, description="Optional name search"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[ProductRead]:
    service = ProductService(db)
    if q:
        return service.search(q)
    return service.list(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductRead:
    try:
        return ProductService(db).get(product_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_active_superuser),
) -> ProductRead:
    return ProductService(db).create(payload)


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_active_superuser),
) -> ProductRead:
    try:
        return ProductService(db).update(product_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_active_superuser),
) -> None:
    try:
        ProductService(db).delete(product_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
