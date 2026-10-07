"""Domain-level exceptions, translated to HTTP responses at the API layer."""


class AppError(Exception):
    """Base class for all application-raised errors."""


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier: object):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with id={identifier!r} not found")


class AlreadyExistsError(AppError):
    """Raised when attempting to create a resource that violates a uniqueness constraint."""

    def __init__(self, resource: str, field: str, value: object):
        self.resource = resource
        self.field = field
        self.value = value
        super().__init__(f"{resource} with {field}={value!r} already exists")


class InsufficientStockError(AppError):
    """Raised when an order requests more units of a product than are in stock."""

    def __init__(self, product_id: int, requested: int, available: int):
        self.product_id = product_id
        self.requested = requested
        self.available = available
        super().__init__(
            f"Product {product_id}: requested {requested}, only {available} in stock"
        )


class InvalidCredentialsError(AppError):
    """Raised when login credentials don't match a known, active user."""
